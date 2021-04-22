import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Mock:
    @staticmethod
    def create_superuser():
        try:
            user = User.objects.create_superuser(username="admin", email="email@email.com.br", password="asdf@1234")
            if user is not None:
                Token.objects.create(user=user, key='2b817ddbb5b974e5a451a8156963de586d72079e')
        except Exception as error:
            print(error)


if __name__ == "__main__":
    Mock().create_superuser()