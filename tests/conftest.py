import uuid
from datetime import datetime
from uuid import UUID

import boto3
import pytest
from pydantic import Field

from coraline import CoralConfig, CoralModel, HashType, KeyField
from coraline.field import TTLField


@pytest.fixture
def user_table():
    class UserTable(CoralModel):
        model_config = CoralConfig(
            aws_endpoint_url="http://localhost:8001",
            aws_access_key_id="DUMMYIDEXAMPLE",
            aws_secret_access_key="DUMMYEXAMPLEKEY",
            aws_region="local",
        )
        user_id: UUID = KeyField(
            default_factory=lambda: uuid.uuid4(),
            hash_type=HashType.HASH,
            alias="userId",
        )
        username: str
        password: str
        score: float

    UserTable.get_or_create_table()
    return UserTable


@pytest.fixture
def redirect_link_table():
    class RedirectLinkTable(CoralModel):
        model_config = CoralConfig(
            aws_endpoint_url="http://localhost:8001",
            aws_access_key_id="DUMMYIDEXAMPLE",
            aws_secret_access_key="DUMMYEXAMPLEKEY",
            aws_region="local",
        )
        code: str = KeyField(
            default_factory=lambda: uuid.uuid4(), hash_type=HashType.HASH
        )
        link: str
        created_at: datetime = Field(default_factory=datetime.utcnow)
        ttl: int = TTLField(default=3600)

    RedirectLinkTable.get_or_create_table()
    return RedirectLinkTable


@pytest.fixture
def user_test(user_table, client, faker):
    passw = faker.password()
    user = user_table(username="foo", password=passw, score=9.5)
    user.get_or_create_table()
    client.put_item(
        TableName=user_table.get_table_name(),
        Item={
            "username": {"S": "foo"},
            "password": {"S": passw},
            "userId": {"S": str(user.user_id)},
            "score": {"N": "9.5"},
        },
    )
    return user


@pytest.fixture(scope="session")
def client():
    yield boto3.client(
        "dynamodb", endpoint_url="http://localhost:8001", region_name="local"
    )


@pytest.fixture(autouse=True)
def clean_db(client):
    if "amazonaws.com" in client._endpoint.host:
        raise ValueError(
            "During Unit Tests, you cannot create a table in AWS. Please use a local DynamoDB."
        )
    yield
    table_info = client.list_tables()
    for table_name in table_info["TableNames"]:
        client.delete_table(TableName=table_name)
