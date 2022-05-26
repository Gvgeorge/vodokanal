import requests
from datetime import datetime
import xml.etree.ElementTree as etree
from django.conf import settings


class Exchanger:
    cbr_url: str
    currency_id: str

    @classmethod
    def get_exchange_data_web(cls, date: datetime.date) -> str:
        pass

    @classmethod
    def parse_web_exchange_data(cls, data: str) -> float:
        pass


class ExchangerUSD(Exchanger):
    cbr_url: str = settings.CBR_URL
    currency_id: str = settings.USD_ID

    @classmethod
    def get_exchange_data_web(cls, date: datetime.date) -> str:
        url = f'{cls.cbr_url}{date.strftime("%d/%m/%Y")}'
        return requests.get(url).text

    @classmethod
    def parse_web_exchange_data(cls, data: str) -> float:
        try:
            root = etree.fromstring(data)
            exchange_rate = root.find(
            f"./Valute[@ID='{cls.currency_id}']").find('Value').text
        except AttributeError:
            raise AttributeError(f'{data}')

        return float(exchange_rate.replace(',', '.'))

