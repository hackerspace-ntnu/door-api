import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
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


class DoorApiView(View):
    def get(self):
        is_open = False  # TODO
        return JsonResponse({
            'open': is_open,
        })

    def post(self):
        return JsonResponse({
            'to': 'do',
        })


urlpatterns = [
    url(r'^api/door/(?P<name>.*)/$', DoorApiView.as_view(), name='door-api'),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
