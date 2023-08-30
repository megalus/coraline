def test_get_record_by_hash_key(user_table, user_test):
    # Arrange

    # Act
    user = user_table.get(user_id=user_test.user_id)

    # Assert
    assert user == user_test


async def test_get_record_by_hash_key_async(user_table, user_test):
    # Arrange

    # Act
    user = await user_table.aget(user_id=user_test.user_id)

    # Assert
    assert user == user_test
