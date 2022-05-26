from django.db import models
from datetime import datetime
from .cbr import ExchangerUSD, Exchanger
from django.conf import settings


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

    @classmethod
    def _update_or_create_from_sheets(cls, row: dict) -> None:
        usd_rate = Rates.get_exchange_rate(row['date'])
        row['amount_rub'] = row['amount_usd'] * usd_rate
        row['amount_usd'] *= 10000
        obj, created = cls.objects.update_or_create(
            order_id=row['order_id'],
            defaults=row
        )

    @classmethod
    def sync_with_sheets(cls, rows: list) -> None:
        db_ids = set([id[0] for id in Order.objects.all().values_list('pk')])
        sheet_ids = [row['order_id'] for row in rows]
        orders_to_delete = db_ids.difference(sheet_ids)
        cls.objects.filter(order_id__in=orders_to_delete).delete()
        for row in rows:
            cls._update_or_create_from_sheets(row)


class Rates(models.Model):
    date = models.DateField(unique=True)
    rate = models.IntegerField()

    exchanger: Exchanger = ExchangerUSD

    @classmethod
    def get_exchange_rate(cls,
                          date: datetime.date,
                          ) -> float:
        print(date)
        obj, created = cls.objects.get_or_create(
            date=date,
            defaults={'rate': cls.exchanger.parse_web_exchange_data(
                            cls.exchanger.get_exchange_data_web(date))*10000
                      })
        return obj.rate
