import time
import os

import telepot
from telepot.loop import MessageLoop

from .models import Order, TGUser


API_TOKEN = os.getenv('TG_API_KEY')
bot = telepot.Bot(API_TOKEN)


def handle(msg):
    '''
    Заносит telegram_id пользователя в БД для последующей рассылки
    '''
    content_type, chat_type, chat_id = telepot.glance(msg)

    if msg['text'] == '/start':
        TGUser.objects.get_or_create(tg_id=chat_id)
    bot.sendMessage(chat_id, 'message received')


def send_order_data():
    '''
    Составляет сообщение о готовности заказов и отсылает его
    '''
    msg = ''
    orders = Order.prepare_query_for_tg_message()
    if orders:
        for order in orders:
            msg += f'Пришел заказ #{order[0]} на сумму {order[1]/10000}\n'
        for user in TGUser.objects.all():
            bot.sendMessage(user.tg_id, msg[:-1])


def main():
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)


