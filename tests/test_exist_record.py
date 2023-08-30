import uuid


def test_exist_record_by_hash_key(user_table, user_test):
    # Arrange

    # Act
    result_true = user_table.exists(user_id=user_test.user_id)
    result_false = user_table.exists(user_id=uuid.uuid4())

    # Assert
    assert result_true is True
    assert result_false is False


async def test_exist_record_by_hash_key_async(user_table, user_test):
    # Arrange

    # Act
    result_true = await user_table.aexists(user_id=user_test.user_id)

    # Assert
    assert result_true is True
