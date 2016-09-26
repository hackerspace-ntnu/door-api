from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View

from door.models import Door
from door.utils import decode_json_bytes


class DoorApiView(View):
    def get(self, *args, name, **kwargs):
        door = Door.objects.get(name=name)

        return JsonResponse(door.get_status_dict())

    def post(self, request, *args, name, **kwargs):
        decoded_body = decode_json_bytes(request.body)

        if decoded_body.get('key') != settings.DOOR_KEY:
            return HttpResponse(status=401)

        door = Door.objects.get(name=name)

        if decoded_body['open']:
            changed = door.open()
        else:
            changed = door.close()

        status_code = 201 if changed else 200
        return JsonResponse(door.get_status_dict(), status=status_code)
