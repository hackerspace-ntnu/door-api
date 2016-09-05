import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic.base import View

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite',
        }
    },
    INSTALLED_APPS=('door',),
)


class ApiView(View):
    def get(self):
        return JsonResponse()

    def post(self):
        return JsonResponse()


urlpatterns = [
    url(r'^api/door/$', ApiView.as_view()),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
