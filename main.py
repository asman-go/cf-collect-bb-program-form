import asyncio
import base64
import json

from src.database import DocumentAPI
from src.queue import SQS
from src.config import Config
from src.models import Form
from src.constants import (
    FORM_PROGRAM_NAME_FIELD,
    FORM_BUGBOUNTY_PLATFORM_FIELD,
    FORM_BUGBOUNTY_PROGRAM_URL,
    FORM_IN_SCOPE_FIELD,
    FORM_MOBILE_SCOPE_FIELD,
    FORM_NOT_PAID_FIELD,
    FORM_OUT_OF_SCOPE_FIELD,
    FORM_NOTES_FIELD,
)


async def task(data, config: Config):
    # 1. Store form to DynamoDB
    print('Upload data to DynamoDB', data.program_name)
    dynamodb = DocumentAPI(config)
    dynamodb.upsert(data)

    # 2. Send domains to SQS
    sqs = SQS(config)
    if data.in_scope:
        domains = json.loads(data.in_scope)
        domains = [
            domain.replace('*.', '').replace('\r', '').strip() 
            for domain in domains
        ]
        domains = list(set(domains))
        print('Upload domains to SQS, count: ', len(domains))
        for domain in domains:
            sqs.send_message(domain)


def event_handler(event, context):
    # print('Event:', event)
    config = Config()
    if 'body' in event:
        data = base64.b64decode(event['body']).decode()
        # data = base64.b64decode(data).decode()
        data = json.loads(data)

        form_data = Form()

        if FORM_PROGRAM_NAME_FIELD in data:
            form_data.program_name = data[FORM_PROGRAM_NAME_FIELD]

        if FORM_BUGBOUNTY_PLATFORM_FIELD in data:
            form_data.platform = data[FORM_BUGBOUNTY_PLATFORM_FIELD]

        if FORM_BUGBOUNTY_PROGRAM_URL in data:
            form_data.program_site = data[FORM_BUGBOUNTY_PROGRAM_URL]

        if FORM_IN_SCOPE_FIELD in data:
            form_data.in_scope = json.dumps(
                data[FORM_IN_SCOPE_FIELD].split('\n')
            )

        if FORM_MOBILE_SCOPE_FIELD in data:
            form_data.mobile_scope = json.dumps(
                data[FORM_MOBILE_SCOPE_FIELD].split('\n')
            )

        if FORM_NOT_PAID_FIELD in data:
            form_data.not_paid_scope = json.dumps(
                data[FORM_NOT_PAID_FIELD].split('\n')
            )

        if FORM_OUT_OF_SCOPE_FIELD in data:
            form_data.out_of_scope = json.dumps(
                data[FORM_OUT_OF_SCOPE_FIELD].split('\n')
            )

        if FORM_NOTES_FIELD in data:
            form_data.notes = data[FORM_NOTES_FIELD]

        asyncio.run(task(form_data, config))

        return {'status': 'OK'}
    
    else:
        return {'status': 'FAIL'}