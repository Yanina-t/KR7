from django.core.management import BaseCommand

from user.utils import MyBot, send_registration_confirmation_email


class Command(BaseCommand):

    def handle(self, *args, **options):
        my_bot = MyBot()
        my_bot.send_message('Hi , test bot =)')

        # send_registration_confirmation_email('yaninatest3@gmail.com')


