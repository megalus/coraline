import uuid
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Tuple

import pytest
from pydantic import UUID4, BaseModel, EmailStr, SecretStr

from coraline import CoralConfig, CoralModel, HashType, KeyField


def test_create_simple_table(user_table, client):
    # Arrange

    # Act
    user_table.get_or_create_table()

    # Assert
    response = client.describe_table(TableName="UserTable")
    assert response["Table"]["TableName"] == "UserTable"


async def test_create_simple_table_async(user_table):
    # Arrange

    # Act
    test_table = await user_table.aget_or_create_table()

    # Assert
    assert test_table["Table"]["TableName"] == "UserTable"


def test_create_table_with_custom_name(client):
    # Arrange
    class TestModel(CoralModel):
        model_config = CoralConfig(
            table_name="MyCustomNameTable",
            aws_region="local",
            aws_endpoint_url="http://localhost:8099",
            aws_access_key_id="DUMMYIDEXAMPLE",
            aws_secret_access_key="DUMMYEXAMPLEKEY",
        )
        foo: str = KeyField(..., hash_type=HashType.HASH)
        bar: str

    # Act
    TestModel.get_or_create_table()

    # Assert
    response = client.describe_table(TableName=TestModel.get_table_name())
    assert response["Table"]["TableName"] == "MyCustomNameTable"


def test_do_not_create_database_in_aws_during_tests():
    # Arrange
    class TestModel(CoralModel):
        model_config = CoralConfig(
            aws_region="us-east-1",
        )
        foo: str = KeyField(..., hash_type=HashType.HASH)
        bar: str

    # Act / Assert
    with pytest.raises(ValueError) as excinfo:
        TestModel.get_or_create_table()
        assert "During Unit Tests, you cannot create a table in AWS." in str(
            excinfo.value
        )


def test_create_fields(faker):
    # Arrange
    class TestEnum(Enum):
        ACTIVE = "active"
        INACTIVE = "inactive"

    class SixModel(BaseModel):
        email: EmailStr
        password: SecretStr
        status: TestEnum

    class TestFieldsModel(CoralModel):
        model_config = CoralConfig(
            aws_region="local",
            aws_endpoint_url="http://localhost:8099",
            aws_access_key_id="DUMMYIDEXAMPLE",
            aws_secret_access_key="DUMMYEXAMPLEKEY",
        )
        field_one: str = KeyField(..., hash_type=HashType.HASH)
        field_two: int = KeyField(..., hash_type=HashType.RANGE)
        field_three: Dict[str, str]
        field_four: List[Dict[str, str]]
        field_five: List[Tuple[bool, Decimal]]
        field_six: Dict[UUID4, List[SixModel]]

    TestFieldsModel.get_or_create_table()

    # Act
    six_key = uuid.uuid4()
    six_value = [
        {
            "email": faker.email(),
            "password": faker.password(),
            "status": TestEnum.ACTIVE,
        }
    ]
    new_record = TestFieldsModel(
        field_one="test",
        field_two=42,
        field_three={"key": "value"},
        field_four=[{"list_key": "list_value"}],
        field_five=[(True, Decimal("19.99"))],
        field_six={six_key: six_value},
    )
    new_record.save()
    saved_record = TestFieldsModel.get(field_one="test", field_two=42)

    # Assert
    assert saved_record.field_one == "test"
    assert saved_record.field_two == 42
    assert saved_record.field_three == {"key": "value"}
    assert saved_record.field_four == [{"list_key": "list_value"}]
    assert saved_record.field_five == [(True, Decimal("19.99"))]
    assert saved_record.field_six[six_key][0].email == six_value[0]["email"]
    assert (
        saved_record.field_six[six_key][0].password.get_secret_value()
        == six_value[0]["password"]
    )
    assert saved_record.field_six[six_key][0].status == TestEnum.ACTIVE
