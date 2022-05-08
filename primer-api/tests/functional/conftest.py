import sys
import os
import boto3
import pytest


def pytest_addoption(parser):
    parser.addoption("--api", action="store")


def pytest_generate_tests(metafunc):
    api = metafunc.config.option.api
    if api:
        metafunc.parametrize("api", [api])
    else:
        sys.exit("--api flag must be set")


def retrieve_api_id(api_name: str) -> str:
    client = boto3.client("apigateway")
    apis = client.get_rest_apis()
    for item in apis["items"]:
        if item["name"] == api_name:
            return item["id"]
    else:
        sys.exit(f"API '{api_name}' doesnt exist on AWS")


def get_invoke_url(
    api_name: str, stage: str = "dev", region: str = "eu-west-1"
) -> str:
    template = "https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"
    api_id = retrieve_api_id(api_name)
    return template.format(api_id=api_id, region=region, stage=stage)


@pytest.fixture
def url(api):
    return get_invoke_url(api)


@pytest.fixture
def api_key(api):
    api_key = os.getenv("API_KEY")
    if "serverless-framework" in api:
        api_key += "2"
    return api_key
