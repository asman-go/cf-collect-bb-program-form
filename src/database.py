import boto3
import typing

from src.config import Config
from src.models import Form
from src.constants import (
    PROGRAMMES_TABLE_NAME, 
    PROGRAMMES_TABLE_KEY_SCHEMA, 
    PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
)


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

    def create_table(self, table_name: str, key_schema, attribute_definitions):
        table = self._resource.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()

        return table

    def get_table(
            self,
            table_name: str,
            key_schema=PROGRAMMES_TABLE_KEY_SCHEMA,
            attribute_definitions=PROGRAMMES_TABLE_ATTRIBUTE_DEFINITIONS
        ):
        tables = self._client.list_tables()['TableNames']
        if table_name not in tables:
            table = self.create_table(
                table_name,
                key_schema,
                attribute_definitions
            )

            return table
        else:
            return self._resource.Table(table_name)
        
    def upsert(self, data: Form):
        print('BB Form:', data)
        table = self.get_table(PROGRAMMES_TABLE_NAME)
        table.put_item(
            Item=data.dict()
        )