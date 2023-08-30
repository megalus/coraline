def test_create_simple_table(user_table, client):
    # Arrange

    # Act
    user_table.get_or_create_table()

    # Assert
    response = client.describe_table(TableName=user_table.model_config["table_name"])
    assert response["Table"]["TableName"] == user_table.model_config["table_name"]


async def test_create_simple_table_async(user_table):
    # Arrange

    # Act
    test_table = await user_table.aget_or_create_table()

    # Assert
    assert test_table["Table"]["TableName"] == user_table.model_config["table_name"]
