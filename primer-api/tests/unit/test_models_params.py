import pytest
from app.models import params
from app.errors import InvalidInputError
from app.settings import limit_settings


def test_validate_params():
    query_params = {"limit": 3}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    assert p.limit == 3


def test_validate_params_default_limit():
    query_params = {}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    assert p.limit == limit_settings["default"]


def test_validate_params_all_params():
    query_params = {"limit": 3, "cursor": "foobar", "merchant": "socart"}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    assert p.limit == 3
    assert p.cursor == "foobar"
    assert p.merchant == "socart"


def test_validate_params_invalid_limits():
    with pytest.raises(InvalidInputError) as e:
        params.validate_params({"limit": 0}, params.TransactionsQueryParams)
    assert e.value.message == "limit: ensure this value is greater than 1"

    with pytest.raises(InvalidInputError) as e:
        params.validate_params(
            {"limit": 10000}, params.TransactionsQueryParams
        )
    assert e.value.message == "limit: ensure this value is less than 1001"


def test_validate_params_invalid_params():
    with pytest.raises(InvalidInputError) as e:
        params.validate_params(
            {"limit": 3, "foo": "bar"}, params.TransactionsQueryParams
        )
    assert e.value.message == "foo: extra fields not permitted"


def test_validate_params_filters():
    query_params = {"merchant": "merch", "amount": "300"}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    filters = p.filters()
    assert len(filters) == 2
    for filter in filters:
        if filter["key"] == "merchant":
            assert filter["value"] == "merch"
        if filter["key"] == "amount":
            assert filter["value"] == 300


def test_validate_params_filters_gte():
    query_params = {"merchant": "merch", "amount": "gte:300"}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    filters = p.filters()
    assert len(filters) == 2
    for filter in filters:
        if filter["key"] == "merchant":
            assert filter["value"] == "merch"
        if filter["key"] == "amount":
            assert filter["value"] == 300
            assert filter["operator"] == "gte"


def test_validate_params_filters_lte():
    query_params = {"merchant": "merch", "amount": "lte:300"}
    p = params.validate_params(query_params, params.TransactionsQueryParams)
    filters = p.filters()
    assert len(filters) == 2
    for filter in filters:
        if filter["key"] == "merchant":
            assert filter["value"] == "merch"
        if filter["key"] == "amount":
            assert filter["value"] == 300
            assert filter["operator"] == "lte"


def test_validate_params_invalid_amount():
    query_params = {"amount": "lt=200"}
    with pytest.raises(InvalidInputError) as e:
        params.validate_params(query_params, params.TransactionsQueryParams)
    assert "string does not match regex" in e.value.message
