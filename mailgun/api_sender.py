import asyncio
import logging
import httpx

from schemas.api import ApiArgs
from typing import List


logger = logging.getLogger(__name__)


async def request(client: httpx.AsyncClient, args: dict):
    if args["request_type"] == "GET":
        return await client.get(args["url"])
    elif args["request_type"] == "POST":
        return await client.post(args["url"])
    elif args["request_type"] == "PUT":
        return await client.put(args["url"])
    elif args["request_type"] == "DELITE":
        return await client.delete(args["url"])


async def send_api(senders: List[ApiArgs]):
    logger.debug(f"senders: {senders}")
    client = httpx.AsyncClient()

    coros = [request(client, i) for i in senders]

    await asyncio.gather(*coros)
