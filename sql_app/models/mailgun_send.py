from datetime import datetime

from sqlalchemy import (
    Table,
    Column, BigInteger, VARCHAR,
    TIMESTAMP, TEXT, BOOLEAN,
    DATE
)

from sql_app.database import metadata


MailgunSend = Table(
    "mailgun_send",
    metadata,
    Column("id", BigInteger, primary_key=True, index=True),
    Column("phone", VARCHAR(55), default="null"),
    Column("email", VARCHAR(255), default="null"),
    Column("created", TIMESTAMP, default=datetime.now()),
    Column("url", TEXT),
    Column("status", BOOLEAN, default=False),
    Column("idcampaign", VARCHAR(55), default="smv"),
    Column("time_send", TIMESTAMP),
    Column("ga", VARCHAR(255)),
    Column("md5", VARCHAR(55)),
    Column("ip", VARCHAR(64)),
    Column("useragent", TEXT),
    Column("date", DATE, default=datetime(year=2019, month=9, day=4)),
    Column("sec", VARCHAR(55)),
    Column("caltat_sid", VARCHAR(255)),
    Column("sonar_sid", VARCHAR(255)),
    Column("pid", VARCHAR(55)),
    Column("operator", VARCHAR),
)
