from datetime import datetime

import pytz
from django.db import models

from .cbr import Exchanger, ExchangerUSD


class Order(models.Model):
    '''
    All currency is stored in 1/10000 of the units
    e.g. 1$ = 10000 currency units stored
    '''
    order_id = models.IntegerField(primary_key=True)
    row_id = models.IntegerField()
    amount_usd = models.IntegerField()
    amount_rub = models.IntegerField()
    date = models.DateField()
    message_sent = models.BooleanField(default=False)

    @classmethod
    def _update_or_create_from_sheets(cls, row: dict) -> None:
        '''
        Записывает строку из google sheets в базу данных
        '''
        usd_rate = Rates.get_exchange_rate(row['date'])
        row['amount_rub'] = row['amount_usd'] * usd_rate
        row['amount_usd'] *= 10000
        obj, created = cls.objects.update_or_create(
            order_id=row['order_id'],
            defaults=row
        )

    @classmethod
    def sync_with_sheets(cls, rows: list) -> None:
        '''
        получает на вход список строк полученных их google sheets
        синхронизирует с ними БД
        '''
        # Удаление
        db_ids = set([id[0] for id in Order.objects.all().values_list('pk')])
        sheet_ids = [row['order_id'] for row in rows]
        orders_to_delete = db_ids.difference(sheet_ids)
        cls.objects.filter(order_id__in=orders_to_delete).delete()
        # добавление/обновление
        for row in rows:
            cls._update_or_create_from_sheets(row)

    @classmethod
    def prepare_query_for_tg_message(cls):
        '''
        Подготавливает данные для рассылки и обновляет поле message_sent
        '''
        timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now().replace(tzinfo=pytz.utc).astimezone(timezone)
        query = cls.objects.filter(date__lte=now).filter(message_sent=False)
        data = list(query.values_list('pk', 'amount_usd'))[:]
        query.update(message_sent=True)
        return data


class Rates(models.Model):
    '''
    так как курс ЦБ задним числом не изменяется, вижу полезным хранить
    его в своей БД.
    курс тоже сохраняется в формате курс*10000
    '''
    date = models.DateField(unique=True)
    rate = models.IntegerField()

    exchanger: Exchanger = ExchangerUSD

    @classmethod
    def get_exchange_rate(cls,
                          date: datetime.date,
                          ) -> float:
        '''
        Возвращает курс на дату из БД, если не находит, то идет на сайт ЦБ,
        получает его там, сохраняет в бд и возвращает.
        '''
        obj, created = cls.objects.get_or_create(
            date=date,
            defaults={'rate': cls.exchanger.parse_web_exchange_data(
                            cls.exchanger.get_exchange_data_web(date))*10000
                      })
        return obj.rate


class TGUser(models.Model):
    '''
    Хранилище telegram chat_id для рассылки.
    '''
    tg_id = models.IntegerField(primary_key=True)
