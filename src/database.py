import boto3
import typing

from src.config import Config
from src.models import Form


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
                KeySchema=[
                    {
                        'AttributeName': 'program_site',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'program_name',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'program_site',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'platform',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'in_scope',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'mobile_scope',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'not_paid_scope',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'out_of_scope',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'notes',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            
            return table
        else:
            return self._resource.Table(PROGRAMMES_TABLE_NAME)
        
    def upsert(self, data: Form):
        table = self.get_table()
        table.put_item(
            Item=data.dict()
        )