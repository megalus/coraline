import arrow


def test_get_ttl_record(redirect_link_table):
    # Arrange
    link = "https://www.google.com"
    now = arrow.utcnow()
    redirect_link = redirect_link_table(
        code="test", link=link, ttl=1, created_at=now.datetime
    )
    redirect_link.save()

    # Act
    test_link = redirect_link_table.get(code="test")
    table_info = redirect_link_table.get_table_info(include=["describe_time_to_live"])
    # Since we can't test the actual TTL, we'll test the status of the TTL
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
    assert table_info["TimeToLiveDescription"]["TimeToLiveStatus"] == "ENABLED"
    assert table_info["TimeToLiveDescription"]["AttributeName"] == "ttl"

    # Assert
    assert test_link == redirect_link
    assert arrow.get(test_link.created_at) == now
