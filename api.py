import sys

from django.conf import settings
from django.core.management import execute_from_command_line

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    DOOR_KEY='door-key',
    ROOT_URLCONF='urls',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite',
        }
    },
    INSTALLED_APPS=('door',),
)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
