from django.conf import settings
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from door.models import Door
from door.utils import decode_json_bytes


class DoorApiView(View):
    def get(self, *args, name, **kwargs):
        door = get_object_or_404(Door, name=name)

        return JsonResponse(door.get_status_dict())

    def post(self, request, *args, name, **kwargs):
        door = get_object_or_404(Door, name=name)

        decoded_body = decode_json_bytes(request.body)

        key = decoded_body.get('key')
        is_open = decoded_body.get('is_open')

        if key is None:
            return HttpResponse('Missing parameter key', status=401)

        if key != settings.DOOR_KEY:
            return HttpResponse('Incorrect key', status=401)

        if is_open is None:
            return HttpResponseBadRequest('Missing parameter is_open', status=400)

        if is_open:
            changed = door.open()
        else:
            changed = door.close()

        status_code = 201 if changed else 200

        return JsonResponse(door.get_status_dict(), status=status_code)
