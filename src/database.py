import boto3
import typing

from src.config import Config


class DocumentAPI(object):

    def __init__(self, config: Config) -> None:
        self._client = boto3.client(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

        self._resource = boto3.resource(
            'dynamodb',
            endpoint_url=config.DOCUMENT_API_ENDPOINT,
            region_name=config.REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )

    def get_table(self):
        PROGRAMMES_TABLE_NAME = f'bbprogrammes'
        tables = self._client.list_tables()['TableNames']
        if PROGRAMMES_TABLE_NAME not in tables:
            table = self._resource.create_table(
                TableName=PROGRAMMES_TABLE_NAME,
                KeySchema=[],
                AttributeDefinitions=[],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            
            return table
        else:
            return self._resource.Table(PROGRAMMES_TABLE_NAME)
        
    def upsert(self, data):
        table = self.get_table()
        table.put_item(
            Item={
                'data': data
            }
        )