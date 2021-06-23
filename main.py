from fastapi import FastAPI

import logging
import sentry_sdk

from config import Config
from sheduler import sheduler_router

from sentry_sdk.integrations.logging import LoggingIntegration


level = logging.DEBUG if Config.DEBUG else logging.INFO

logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=level,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn="https://dd88228d44c14795b0ae0358a5541e2b@sentry.caltat.com/7",
    integrations=[sentry_logging]
)

app = FastAPI(title="Caltat mailgun sheduller", version="2021.03.15",
              description="Service for the API for send data to clients")

app.include_router(sheduler_router.router)
