import asyncio
import itertools
import typing

from src.database import DocumentAPI
from src.config import Config


async def task(data, config: Config):
    dynamodb = DocumentAPI(config)
    dynamodb.upsert(data)


def event_handler(event, context):
    config = Config()
    asyncio.run(task(event, config))
    return {
        'response': {
            'data': event
        }
    }