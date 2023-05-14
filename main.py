import asyncio
import base64
import json

from src.database import DocumentAPI
from src.config import Config
from src.models import Form


async def task(data, config: Config):
    dynamodb = DocumentAPI(config)
    dynamodb.upsert(data)


def event_handler(event, context):
    print('Event:', event)
    config = Config()
    if 'body' in event:
        data = base64.b64decode(event['body']).decode()
        # data = base64.b64decode(data).decode()
        data = json.loads(data)

        form_data = Form()

        if 'Название Bug Bounty программы' in data:
            form_data.program_name = data['Название Bug Bounty программы']

        if 'Bug Bounty платформа' in data:
            form_data.platform = data['Bug Bounty платформа']

        if 'Ссылка на BugBounty программу' in data:
            form_data.program_site = data['Ссылка на BugBounty программу']

        if 'In scope' in data:
            form_data.in_scope = data['In scope']

        if 'Mobile Scope' in data:
            form_data.mobile_scope = data['Mobile Scope']

        if 'Not paid' in data:
            form_data.not_paid_scope = data['Not paid']

        if 'Out of scope' in data:
            form_data.out_of_scope = data['Out of scope']

        if 'Замечания' in data:
            form_data.notes = data['Замечания']

        asyncio.run(task(form_data, config))

        return {'status': 'OK'}
    
    else:
        return {'status': 'FAIL'}