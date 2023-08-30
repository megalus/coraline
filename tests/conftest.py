import uuid
from uuid import UUID

import boto3
import pytest
import stringcase

from coraline import CoralConfig, CoralModel, HashType, KeyField


@pytest.fixture
def user_table(faker):
    table_name = stringcase.camelcase(
        faker.sentence(nb_words=3, variable_nb_words=False)
    )

    class UserTable(CoralModel):
        model_config = CoralConfig(
            table_name=table_name,
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

    return UserTable


@pytest.fixture
def user_test(user_table, client, faker):
    passw = faker.password()
    user = user_table(username="foo", password=passw)
    user.get_or_create_table()
    client.put_item(
        TableName=user_table.model_config["table_name"],
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
