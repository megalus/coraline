from decimal import Decimal

import arrow


def test_delete_record(user_table, user_test, client, faker):
    # Arrange
    created_at = arrow.utcnow().datetime
    foo_user = user_table(
        username="foo",
        password=faker.password(),
        score=7.75,
        created_at=created_at,
        price=Decimal("19.99"),
    )
    foo_user.save()

    # Act
    foo_user.delete()

    # Assert
    assert user_table.exists(user_id=foo_user.user_id) is False
    assert user_table.exists(user_id=user_test.user_id) is True


async def test_delete_record_async(user_table, user_test, client, faker):
    # Arrange
    created_at = arrow.utcnow().datetime
    foo_user = user_table(
        username="foo",
        password=faker.password(),
        score=7.75,
        created_at=created_at,
        price=Decimal("19.99"),
    )
    await foo_user.asave()

    # Act
    await foo_user.adelete()

    # Assert
    assert await user_table.aexists(user_id=foo_user.user_id) is False
    assert await user_table.aexists(user_id=user_test.user_id) is True
