def test_save_record(user_table, client, faker):
    # Arrange

    # Act
    new_user = user_table(username="foo", password=faker.password(), score=7.75)
    new_user.save()
    key_data = {"userId": {"S": str(new_user.user_id)}}
    user_on_disk = client.get_item(TableName=user_table.get_table_name(), Key=key_data)

    # Assert
    assert str(new_user.user_id) == user_on_disk["Item"]["userId"]["S"]
    assert user_on_disk["Item"]["score"]["N"] == str(7.75)


async def test_save_record_async(user_table, client, faker):
    # Arrange

    # Act
    new_user = user_table(username="foo", password=faker.password(), score=7.75)
    await new_user.asave()

    user_on_disk = await user_table.aget(user_id=new_user.user_id)

    # Assert
    assert new_user == user_on_disk
