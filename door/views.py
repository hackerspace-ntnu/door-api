from django.http.response import JsonResponse
from django.views.generic.base import View


class DoorApiView(View):
    def get(self, *args, **kwargs):
        return JsonResponse({
            'to': 'do',
        })

    def post(self, *args, **kwargs):
        return JsonResponse({
            'to': 'do',
        })
