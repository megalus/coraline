import uuid
from uuid import UUID

import boto3
import pytest

from coraline import CoralConfig, CoralModel, HashType, KeyField


@pytest.fixture
def user_table():
    class UserTable(CoralModel):
        model_config = CoralConfig(
            aws_endpoint_url="http://localhost:8000",
            aws_region="local",
        )
        user_id: UUID = KeyField(
            default_factory=lambda: uuid.uuid4(),
            hash_type=HashType.HASH,
            alias="userId",
        )
        username: str
        password: str

    UserTable.get_or_create_table()
    return UserTable


@pytest.fixture
def user_test(user_table, client, faker):
    passw = faker.password()
    user = user_table(username="foo", password=passw)
    user.get_or_create_table()
    client.put_item(
        TableName=user_table.get_table_name(),
        Item={
            "username": {"S": "foo"},
            "password": {"S": passw},
            "userId": {"S": str(user.user_id)},
        },
    )
    return user


@pytest.fixture(scope="session")
def client():
    yield boto3.client(
        "dynamodb", endpoint_url="http://localhost:8000", region_name="local"
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
