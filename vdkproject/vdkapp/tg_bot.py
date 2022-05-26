
from .models import Order, TGUser
import telepot
from telepot.loop import MessageLoop
import time

API_TOKEN = '5363088590:AAHQpK6G30VyGQvo0kEWJk2ZyLE2JnWkKkw'

# Initialize bot and dispatcher


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




