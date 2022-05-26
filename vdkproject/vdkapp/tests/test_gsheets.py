import pytest
from vdkapp.sheets import create_gsheets_service, read_values, parse_values_for_db
from datetime import date
from django.conf import settings
from apiclient.discovery import Resource, build
from django.core.exceptions import ValidationError



def test_create_gsheets_service():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    assert type(service) == Resource


def test_read_values():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_read', 'A', 'D')
    values = response['valueRanges'][0]['values'][1:]
    assert len(values) == 2
    assert values[0][1] == '1249708'


def test_empty_string():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_empty', 'A', 'D')
    values = parse_values_for_db(response)
    assert len(values) == 2


def test_parse_values_for_db():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_read', 'A', 'D')
    values = parse_values_for_db(response)
    assert values[0] == {
        'row_id': 1,
        'order_id': 1249708,
        'amount_usd': 675.0,
        'date': date(2022, 5, 24)
        }

