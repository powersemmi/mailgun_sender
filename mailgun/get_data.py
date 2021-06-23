import io
import csv

from typing import Iterable, List
from datetime import datetime

from sqlalchemy.orm import load_only
from sqlalchemy.orm.session import Session

from sql_app.models.mailgun_send import MailgunSend


def get_mailgun_send(db: Session, fields: List[str], limit: int):
    res = db.query(MailgunSend).options(load_only(*fields)).limit(limit).all()

    for i in res:
        yield i.__dict__


def get_test_data(db: Session, fields: List[str], limit: int):
    test_data = [
        {"phone": "88005553535", "email": "foo@bar.com"},
        {"phone": "88005553535", "email": "foo@bar.com"},
        {"phone": "88005553535", "email": "foo@bar.com"},
        {"phone": "88005553535", "email": "foo@bar.com"},
    ]

    for i in test_data[:limit]:
        yield {key: i[key] for key in fields}


def dict_to_csv_buffer(data: Iterable) -> io.BytesIO:
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    keys_flag = True
    for data in data:
        if isinstance(data, dict):
            if keys_flag:
                writer.writerow(data)
                keys_flag = False
            writer.writerow(data.values())
        else:
            writer.writerow(data)

    mem = io.BytesIO()
    mem.name = datetime.now().strftime("%Y-%m-%d") + ".csv"
    mem.write(buffer.getvalue().encode())
    mem.seek(0)
    buffer.close()
    return mem


def get_data(table: str, db: Session, fields: List[str], limit: int = 1000):
    if table == "mailgun_send":
        return get_mailgun_send(db, fields, limit)
    elif table == "test":
        return get_test_data(db, fields, limit)
