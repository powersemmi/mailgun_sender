import logging
import asyncio

from sql_app.database import get_db
from tabulate import tabulate

import httpx

from typing import List

from sqlalchemy.orm.session import Session

from schemas.mail import MailArgs
from mailgun.get_data import get_data, dict_to_csv_buffer

from config import Config

logger = logging.getLogger(__name__)


async def mailgun_api_mail(client: httpx.AsyncClient, args: MailArgs,
                           db: Session):
    files = []
    data = get_data(args.table, db, fields=args.fields, limit=args.limit)
    body = args.body

    if args.concat_type == "attach":
        files.append(('attachment', dict_to_csv_buffer(data)))
    elif args.concat_type == "inline":
        data = list(data)
        body += "\n"*3
        body += '{table}'
        data_new = []
        for i in data:
            data_new.append(list(i.values()))
        body = body.format(table=tabulate(data_new, headers=data[0].keys(),
                                          tablefmt="grid"))

        # TODO: add html format for massages
        # html = body.format(table=tabulate(data, headers="firstrow",
        #                                   tablefmt="html"))

    return await client.post(
        f"https://api.mailgun.net/v3/{args.host}/messages",
        auth=("api", Config.MAILGUN_API),
        data={"from": f"noreply@{args.host}",
              "to": args.to,
              "subject": args.subject,
              "text": body},
        files=files)


async def send_mail(senders: List[MailArgs],
                    db: Session = get_db().__next__()):
    logger.debug(f"senders: {senders}")
    client = httpx.AsyncClient()

    coros = [mailgun_api_mail(client, i, db) for i in senders]
    res = await asyncio.gather(*coros)
    await client.aclose()
    return res
