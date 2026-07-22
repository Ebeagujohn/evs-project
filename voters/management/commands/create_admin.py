from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from decouple import config


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = str(config('ADMIN_USERNAME', default=''))
        password = str(config('ADMIN_PASSWORD', default=''))
        email = str(config('ADMIN_EMAIL', default=''))

        if username and password and not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write('Superuser created')
        else:
            self.stdout.write('Superuser already exists or env vars missing')