
import time
import os

import telepot
from telepot.loop import MessageLoop

from .models import Order, TGUser

API_TOKEN = os.getenv('TG_API_KEY')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if msg['text'] == '/start':
        TGUser.objects.get_or_create(tg_id=chat_id)
 

def send_order_data():
    msg = ''
    orders = Order.prepare_query_for_tg_message()
    if orders:
        for order in orders:
            msg += f'Пришел заказ #{order[0]} на сумму {order[1]/10000}\n'
        for user in TGUser.objects.all():
            bot.sendMessage(user.tg_id, msg[:-1])


bot = telepot.Bot(API_TOKEN)


def main():
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')
    while 1:
        time.sleep(10)


