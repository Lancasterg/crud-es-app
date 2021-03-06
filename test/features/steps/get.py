import urllib

from behave import *
from elasticsearch import Elasticsearch
from src.utils.es_interface import ElasticInterface
from requests import get, put

# Scenario: File does not exist
from src.utils.io_interface import InputOutputInterface


@given('The ES server and REST API are online')
def step_impl(context):
    r = get('http://127.0.0.1:5000/', params={"file_id": "ping"})
    es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)

    if not es.ping():
        raise ValueError("Connection failed")

    assert r.status_code == 200


@when('We send a bad get request')
def step_impl(context):
    r = get('http://127.0.0.1:5000/', params={"file_id": "file_doesnt_exist"})
    context.config.bad_request = r.status_code


@then('We receive a 404 status code')
def step_impl(context):
    assert context.config.bad_request == 404


# Scenario: File does exist

@when('We send a get request')
def step_impl(context):
    headers = {'Content-Type': 'multipart/form-data', 'Slug': 'uploaded_file.txt'}
    r = put('http://127.0.0.1:5000/', data=open('upload_file.txt', 'rb'), headers=headers)
    assert r.status_code == 200

    r = get('http://127.0.0.1:5000/', params={"file_id": "file_doesnt_exist"})


@then('We receive the file and a 200 status code')
def step_impl(context):
    print()
