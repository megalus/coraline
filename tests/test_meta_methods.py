from coraline import CoralModel, HashType, KeyField


def test_get_hash_field():
    # Arrange
    class TestModel(CoralModel):
        foo: str = KeyField(..., hash_type=HashType.HASH)
        bar: str = KeyField(..., hash_type=HashType.RANGE)

    # Act
    hash_field = TestModel.get_hash_field_name()
    range_field = TestModel.get_range_field_name()

    # Assert
    assert hash_field == "foo"
    assert range_field == "bar"
