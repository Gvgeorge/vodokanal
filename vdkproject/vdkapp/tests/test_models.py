import pytest
from vdkapp.models import Order, Rates
from vdkapp.sheets import create_gsheets_service, read_values, parse_values_for_db
from django.conf import settings
from datetime import datetime


pytestmark = pytest.mark.django_db

@pytest.fixture
def read_fixture():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_read', 'A', 'D')
    values = parse_values_for_db(response)
    Order.sync_with_sheets(values)


@pytest.fixture
def update_fixture(read_fixture):
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_update', 'A', 'D')
    values = parse_values_for_db(response)
    Order.sync_with_sheets(values)


@pytest.fixture
def delete_fixture(read_fixture):
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_delete', 'A', 'D')
    values = parse_values_for_db(response)
    Order.sync_with_sheets(values)


@pytest.fixture
def empty_fixture():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'test_empty', 'A', 'D')
    values = parse_values_for_db(response)
    Order.sync_with_sheets(values)


@pytest.mark.django_db
class TestDB:
    pytestmark = pytest.mark.django_db

    def test_read(self, read_fixture):
        assert len(Order.objects.all()) == 2
        row = Order.objects.get(pk=1249708)
        rate = Rates.objects.get(date=datetime.strptime(
            '24.05.2022', '%d.%m.%Y').date())
        assert row.amount_usd == 6750000
        assert row.amount_rub == 392908725
        assert rate.rate == 582087

    def test_update(self, update_fixture):
        assert len(Order.objects.all()) == 3
        row = Order.objects.get(pk=1182407)
        rate = Rates.objects.get(date=datetime.strptime(
            '13.05.2022', '%d.%m.%Y').date())
        assert row.amount_usd == 7770000
        assert row.amount_rub == 511200732
        assert rate.rate == 657916

    def test_update_date(self, update_fixture):
        row = Order.objects.get(pk=1249708)
        rate = Rates.objects.get(date=datetime.strptime(
            '13.05.2022', '%d.%m.%Y').date())
        assert row.amount_usd == 6750000
        assert row.amount_rub == 444093300
        assert rate.rate == 657916

    def test_delete(self, delete_fixture):
        assert len(Order.objects.all()) == 1
        with pytest.raises(Order.DoesNotExist):
            Order.objects.get(pk=1182407)

    def test_empty(self, empty_fixture):
        assert len(Order.objects.all()) == 2
