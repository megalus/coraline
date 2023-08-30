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
            aws_endpoint_url="http://localhost:8000",
        )
        foo: str = KeyField(..., hash_type=HashType.HASH)
        bar: str

    # Act
    TestModel.get_or_create_table()

    # Assert
    response = client.describe_table(TableName=TestModel.get_table_name())
    assert response["Table"]["TableName"] == "MyCustomNameTable"