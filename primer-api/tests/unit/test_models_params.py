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
        params.validate_params({"limit": 200}, params.TransactionsQueryParams)
    assert e.value.message == "limit: ensure this value is less than 101"


def test_validate_params_invalid_params():
    with pytest.raises(InvalidInputError) as e:
        params.validate_params(
            {"limit": 3, "foo": "bar"}, params.TransactionsQueryParams
        )
    assert e.value.message == "foo: extra fields not permitted"
