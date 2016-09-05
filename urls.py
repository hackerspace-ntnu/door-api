from django.conf.urls import url

from door.views import DoorApiView

urlpatterns = [
    url(r'^api/door/(?P<name>.*)/$', DoorApiView.as_view(), name='door-api'),
]
