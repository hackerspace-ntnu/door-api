from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View

from door.models import Door
from door.utils import decode_json_bytes


class DoorApiView(View):
    def get(self, *args, **kwargs):
        name = kwargs.get('name')
        door = Door.objects.get(name=name)

        return JsonResponse({
            'open': door.is_open(),
        })

    def post(self, request, *args, **kwargs):
        decoded_body = decode_json_bytes(request.body)

        if 'key' not in decoded_body or decoded_body['key'] != settings.DOOR_KEY:
            return HttpResponse(status=401)

        name = kwargs.get('name')
        door = Door.objects.get(name=name)

        if decoded_body['open']:
            door.open()
        else:
            door.close()

        return JsonResponse({
            'open': door.is_open(),
        }, status=201)
