import pydantic
import typing


class Config(pydantic.BaseSettings):
    # YDB: via cli — ydb config profile get db1
    DOCUMENT_API_ENDPOINT: str = "https://example.com/path/to/your/db"
    REGION_NAME: str = "ru-central1"
    AWS_ACCESS_KEY_ID: str = "<key-id>"
    AWS_SECRET_ACCESS_KEY: str = "<secret-access-key>"

    SQS_QUEUE_URL: str
