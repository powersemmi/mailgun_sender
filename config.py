from os import environ, path
from dotenv import load_dotenv

load_dotenv()

basedir = path.abspath(path.dirname(__file__))


class Config:
    DEBUG = True if environ.get("DEBUG") == "1" else False
    DATABASE_URL = (environ.get('DATABASE_URL') or 'sqlite:///' +
                    path.join(basedir, 'app.sqlite') +
                    '?check_same_thread=False')
    SHEDULE_DB = (environ.get('SHEDULE_DB') or 'sqlite:///' +
                  path.join(basedir, 'app.sqlite') +
                  '?check_same_thread=False')
    DEFAULT_EMAIL = environ.get("DEFAULT_EMAIL")
    MAILGUN_API = environ.get("MAILGUN_API")
