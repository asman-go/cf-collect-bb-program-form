import asyncio
import base64
import itertools
import typing

from src.database import DocumentAPI
from src.config import Config


async def task(data, config: Config):
    dynamodb = DocumentAPI(config)
    dynamodb.upsert(data)


def event_handler(event, context):
    config = Config()
    if 'body' in event:
        data = base64.b64decode(event['body'])
        asyncio.run(task(data, config))

        return {'status': 'OK'}
    
    else:
        return {'status': 'FAIL'}