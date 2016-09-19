from django.http.response import JsonResponse
from django.views.generic.base import View

from door.models import Door


class DoorApiView(View):
    def get(self, *args, **kwargs):
        name = kwargs.get('name')
        door = Door.objects.get(name=name)

        return JsonResponse({
            'open': door.is_open(),
        })

    def post(self, *args, **kwargs):
        return JsonResponse({
            'to': 'do',
        })
