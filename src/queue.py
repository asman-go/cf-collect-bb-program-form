import boto3

from src.config import Config


class SQS(object):

    def __init__(self, config: Config) -> None:
        self._client = boto3.client(
            'sqs',
            endpoint_url=config.SQS_SERVER_ENDPOINT,
            region_name=config.REGION_NAME
        )

        self._sqs_queue_url = config.SQS_QUEUE_URL

    def send_message(self, domain: str):
        self._client.send_message(
            QueueUrl=self._sqs_queue_url,
            # DelaySeconds=3,
            MessageAttributes={},
            MessageBody=(
                domain
            )
        )