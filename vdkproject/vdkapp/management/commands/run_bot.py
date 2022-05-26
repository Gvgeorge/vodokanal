from vdkapp.tg_bot import main
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs the bot!'

    def handle(self, *args, **options):
        main()