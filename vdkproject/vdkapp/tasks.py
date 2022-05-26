from .sheets import create_gsheets_service, read_values, parse_values_for_db
from django.conf import settings
from .models import Order
from celery import shared_task
from .tg_bot import send_order_data


@shared_task
def update_order_table():
    service = create_gsheets_service(settings.CREDENTIALS_FILE)
    response = read_values(
        service, settings.SPREADSHEET_ID, 'Лист1', 'A', 'D')
    values = parse_values_for_db(response)
    Order.sync_with_sheets(values)


@shared_task
def send_report():
    send_order_data()
