import logging

from time import sleep
from datetime import datetime
from typing import Union

from apscheduler.job import Job
from fastapi import APIRouter, HTTPException

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from config import Config

from mailgun.api_sender import send_api
from mailgun.mail_sender import send_mail

from extra_utils.parse import parse_time

from schemas.sheduler import (
    JobCreateDelete,
    ScheduledJobs,
    NewScheduledJobItem
)

from sql_app import database

logger = logging.getLogger(__name__)

Schedule: AsyncIOScheduler = None

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
async def load_schedule_or_create_blank():
    """
    Instatialise the Schedule Object as a Global Param and also
    load existing Schedules from PostgresSql
    This allows for persistent schedules across server restarts.
    """
    global Schedule
    try:
        jobstores = {
            'default': SQLAlchemyJobStore(url=Config.SHEDULE_DB)
        }
        Schedule = AsyncIOScheduler(jobstores=jobstores)
        trys = 0
        while trys < 10:
            try:
                Schedule.start()
                break
            except Exception as e:
                logger.error(e)
                sleep(5)
                trys += 1
        logger.info("Created Schedule Object")
    except Exception as e:
        logger.error(f"{e}: Unable to Create Schedule Object")


@router.on_event("shutdown")
async def pickle_schedule():
    """
    An Attempt at Shutting down the schedule to avoid orphan jobs
    """
    global Schedule
    Schedule.shutdown()
    logger.info("Disabled Schedule")


@router.get("/api", tags=["schedule"], response_model=ScheduledJobs)
async def get_scheduling():
    """
    Will provide a list of currently Scheduled Tasks
    """
    schedules = []
    for job in Schedule.get_jobs():
        schedules.append({
            "job_id": str(job.id),
            "run_frequency": str(job.trigger),
            "next_run": str(job.next_run_time)
        })
    return {"jobs": schedules}


@router.post("/api", tags=["schedule"], response_model=JobCreateDelete)
async def add_scheduling(job_args: NewScheduledJobItem,
                         db: Session = Depends(get_db)):
    """
    Add a New Job to a Schedule
    """
    assert job_args.trigger in ("cron", "date", "interval"), \
        HTTPException(422, f"trigger {job_args.trigger} is not defined")
    assert job_args.args, HTTPException(422, "args is enmpty")

    if job_args.type == "mail":
        schedule_func = send_mail
    elif job_args.type == "api":
        schedule_func = send_api
    else:
        raise HTTPException(422, f"type {job_args.type} is not defined")

    interval: Union[CronTrigger, datetime, IntervalTrigger]
    try:
        if job_args.trigger == "cron":
            interval = CronTrigger.from_crontab(job_args.interval)
        elif job_args.trigger == "date":
            interval = datetime.strptime(job_args.interval,
                                         job_args.timeformat)
        elif job_args.trigger == "interval":
            parsed_time = parse_time(job_args.interval)
            interval = IntervalTrigger(**parsed_time)

        schedule: Job = Schedule.add_job(schedule_func, interval,
                                         id=job_args.job_id,
                                         kwargs={"senders": job_args.args})
        return {"scheduled": True, "job_id": schedule.id}
    except ConflictingIdError:
        raise HTTPException(422, f"{job_args.job_id} is already exist")


@router.delete("/api", tags=["schedule"], response_model=JobCreateDelete)
async def delete_scheduling(job_id: str):
    """
    Remove a Job from a Schedule
    """
    try:
        Schedule.remove_job(job_id)
    except JobLookupError:
        raise HTTPException(404, f"job_id: {job_id} not found")
    return {"scheduled": False, "job_id": job_id}


@router.put("/api", tags=["schedule"])
async def update_scheduling():
    ...
