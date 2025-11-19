import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

import boto3
import pytest
from arrow import Arrow
from pydantic import EmailStr, Field, SecretStr
from pydantic_extra_types.payment import PaymentCardNumber
from pydantic_extra_types.phone_numbers import PhoneNumber

from coraline import CoralConfig, CoralModel, HashType, KeyField
from coraline.field import TTLField


@pytest.fixture
def user_table():
    class UserTable(CoralModel):
        model_config = CoralConfig(
            aws_endpoint_url="http://localhost:8099",
            aws_access_key_id="DUMMYIDEXAMPLE",
            aws_secret_access_key="DUMMYEXAMPLEKEY",
            aws_region="local",
            protect_from_exclusion=False,
            arbitrary_types_allowed=True,
        )
        user_id: UUID = KeyField(
            default_factory=lambda: uuid.uuid4(),
            hash_type=HashType.HASH,
            alias="userId",
        )
        username: str
        password: SecretStr
        score: float
        price: Decimal
        created_at: datetime | Arrow | int
        order: int = Field(default=1)

        # Optional Extra Fields
        # https://docs.pydantic.dev/2.3/usage/types/extra_types/extra_types/
        secret: Optional[SecretStr] = None
        email: Optional[EmailStr] = None
        phone: Optional[PhoneNumber] = None
        credit_card: Optional[PaymentCardNumber] = None

    UserTable.get_or_create_table()
    return UserTable


@pytest.fixture
def redirect_link_table():
    class RedirectLinkTable(CoralModel):
        model_config = CoralConfig(
            aws_endpoint_url="http://localhost:8099",
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
    now = datetime.now()
    passw = faker.password()
    user = user_table(
        username="foo",
        password=passw,
        score=9.5,
        price=19.99,
        created_at=now.isoformat(),
    )
    user.get_or_create_table()
    client.put_item(
        TableName=user_table.get_table_name(),
        Item={
            "username": {"S": "foo"},
            "password": {"S": passw},
            "userId": {"S": str(user.user_id)},
            "score": {"N": "9.5"},
            "created_at": {"S": now.isoformat()},
            "price": {"N": "19.99"},
        },
    )
    return user


@pytest.fixture(scope="session")
def client():
    yield boto3.client(
        "dynamodb", endpoint_url="http://localhost:8099", region_name="local"
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
