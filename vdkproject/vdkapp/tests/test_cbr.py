import pytest
from vdkapp.cbr import ExchangerUSD
from datetime import date
from django.conf import settings


def test_get_exchange_data_correct() -> None:
    # exchanger = ExchangerUSD()
    day = date(2022, 5, 22)
    assert (settings.USD_ID in ExchangerUSD.get_exchange_data_web(day)) == True


def test_get_exchange_data_wrong_format() -> None:
    with pytest.raises(ValueError):
        ExchangerUSD.get_exchange_data_web(date(2022, 25, 22))
    with pytest.raises(AttributeError):
        ExchangerUSD.get_exchange_data_web('2022-02-02')


def test_get_exchange_data_data_too_early() -> None:
    day = date(1952, 5, 17)
    response = ExchangerUSD.get_exchange_data_web(day)
    assert (settings.USD_ID not in response) == True


def test_get_exchange_data_data_too_high() -> None:
    day = date(2052, 5, 17)
    response = ExchangerUSD.get_exchange_data_web(day)
    assert (settings.USD_ID not in response) == True


def test_parse_exchange_data():
    data = ExchangerUSD.get_exchange_data_web(date(2022, 5, 21))
    assert (ExchangerUSD.parse_web_exchange_data(data)) == 58.8862
