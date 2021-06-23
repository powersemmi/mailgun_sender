import uuid

from typing import List, Union, Literal
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from schemas.mail import MailArgs
from schemas.api import ApiArgs


class JobCreateDelete(BaseModel):
    scheduled: bool = Field(title="Whether the job was scheduler or not",
                            description="Whether the job was scheduler or not")
    job_id: str = Field(title="The Job ID in APScheduler",
                        description="The Job ID in APScheduler")

    class Config:
        schema_extra = {
            'example': {
                'scheduled': True,
                'job_id': "www.google.com"
            }}


class CurrentScheduledJob(BaseModel):
    job_id: str = Field(title="The Job ID in APScheduler",
                        description="The Job ID in APScheduler")
    run_frequency: str = Field(title="The Job Interval in APScheduler",
                               description="The Job Interval in APScheduler")
    next_run: str = Field(title="Next Scheduled Run for the Job",
                          description="Next Scheduled Run for the Job")

    class Config:
        schema_extra = {
             'example': {
                 "job_id": "www.google.com",
                 "run_frequency": "interval[0:05:00]",
                 "next_run": "2020-11-10 22:12:09.397935+10:00"
             }}


class ScheduledJobs(BaseModel):
    jobs: List[CurrentScheduledJob]


class NewScheduledJobItem(BaseModel):
    job_id: str = Field(title="The Job ID in APScheduler",
                        description="The Job ID in APScheduler",
                        default=str(uuid.uuid4()))
    type: Literal['api', 'mail'] = Field(
                      title="Type of Sending Job",
                      description="Type of Sending Job\nMaybe: api|mail")
    name: str = Field("", title="Name of Sending Job",
                      description="Name of Sending Job")
    trigger: Literal["cron", "date", "interval"] = Field(
                        title="The Job trigger type",
                        description="The Job trigger type\n"
                                    "Maybe: cron|date|interval")
    interval: str = Field(title="The Job interval",
                          description="The Job interval\n"
                                      "Maybe: as cron|"
                                      "as date with timeformat|"
                                      "as interval (1w1d1h1m)")
    timeformat: str = Field(title="The python datetime format",
                            description="The python datetime format\n"
                                        "Default: '%d.%m.%y %H:%M:%S'",
                            default='%d.%m.%y %H:%M:%S')
    start_date: str = Field(datetime.now().strftime('%d.%m.%y %H:%M:%S'),
                            title="The date of start job",
                            description="The date of start job")
    end_date: str = Field(
        (datetime.now() + timedelta(days=1)).strftime('%d.%m.%y %H:%M:%S'),
        title="The date of end job",
        description="The date of end job")

    args: Union[List[MailArgs], List[ApiArgs]]

    class Config:
        schema_extra = {
            "example": {
                "job_id": "Test",
                "type": "mail",
                "name": "FooBar",
                "trigger": "interval",
                "interval": "1m",
                "args": [
                    {
                        "to": ["powersemmi@gmail.com"],
                        "host": "post.alphastream.ru",
                        "subject": "FOOOOBAAAR",
                        "body": "foobar is watching you",
                        "concat_type": "inline",
                        "table": "test",
                        "fields": ["phone", "email"],
                        "limit": 300
                    },
                    {
                        "to": ["powersemmi@gmail.com"],
                        "host": "post.alphastream.ru",
                        "subject": "FOOOOBAAAR",
                        "header": "FOOOOBAAAR",
                        "body": "foobar is watching you",
                        "concat_type": "attach",
                        "table": "test",
                        "fields": ["phone", "email"],
                        "limit": 100000
                    },
                ],
            }
        }
