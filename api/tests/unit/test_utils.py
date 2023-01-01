from app.utils import endpoint


def test_endpoint():
    def wee_func(event, context):
        return {"hello": "world"}, 200

    func = endpoint(wee_func)
    exec_func = func(None, None)
    assert exec_func["statusCode"] == 200
    assert exec_func["body"] == '{"hello": "world"}'


def test_endpoint_error():
    def wee_func(event, context):
        raise Exception

    func = endpoint(wee_func)
    exec_func = func(None, None)
    assert exec_func["statusCode"] == 500
    assert (
        exec_func["body"]
        == '{"message": "Unexpected error", "status_code": 500}'
    )  # noqa
