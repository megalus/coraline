import datetime
from decimal import Decimal

import arrow
import pytest


@pytest.mark.parametrize(
    "created_at_fn",
    [
        lambda: arrow.now().int_timestamp,
        lambda: arrow.now(),
        lambda: datetime.datetime.now(datetime.UTC),
        lambda: datetime.datetime.now(datetime.UTC).isoformat(),
    ],
)
def test_save_record(user_table, client, faker, created_at_fn):
    # Arrange
    created_at = created_at_fn()

    # Act
    new_user = user_table(
        username="foo",
        password=faker.password(),
        score=7.75,
        created_at=created_at,
        price=Decimal("19.99"),
    )
    new_user.save()
    key_data = {"userId": {"S": str(new_user.user_id)}}
    user_on_disk = client.get_item(TableName=user_table.get_table_name(), Key=key_data)
    load_user = user_table.get(user_id=new_user.user_id)

    # Assert
    assert str(new_user.user_id) == user_on_disk["Item"]["userId"]["S"]
    assert user_on_disk["Item"]["score"]["N"] == str(7.75)
    assert load_user.order == 1
    assert load_user.price == Decimal("19.99")
    assert load_user.secret is None
    assert load_user.email is None
    assert load_user.phone is None
    assert load_user.credit_card is None
    assert arrow.get(load_user.created_at) == arrow.get(created_at)


def save_optional_fields(user_table, faker):
    # Arrange
    fake_email = faker.email()
    fake_secret = faker.password()
    fake_phone = faker.phone_number()
    fake_credit_card = faker.credit_card_number()
    created_at = arrow.now().int_timestamp

    # Act
    new_user = user_table(
        username="foo",
        password=faker.password(),
        score=7.75,
        created_at=created_at,
        price=Decimal("19.99"),
        secret=fake_secret,
        email=fake_email,
        phone=fake_phone,
        credit_card=fake_credit_card,
    )
    new_user.save()
    load_user = user_table.get(user_id=new_user.user_id)

    # Assert
    assert load_user.secret.get_secret_value() == fake_secret
    assert load_user.email == fake_email
    assert load_user.phone == fake_phone
    assert load_user.credit_card.number == fake_credit_card


async def test_save_record_async(user_table, client, faker):
    # Arrange
    fake_email = faker.email()
    fake_secret = faker.password()
    created_at = arrow.now().int_timestamp

    # Act
    new_user = user_table(
        username="foo",
        password=faker.password(),
        score=7.75,
        secret=fake_secret,
        email=fake_email,
        created_at=created_at,
        price=Decimal("19.99"),
    )
    await new_user.asave()

    user_on_disk = await user_table.aget(user_id=new_user.user_id)

    # Assert
    assert new_user == user_on_disk
