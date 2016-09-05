from django.db.models.base import Model
from django.db.models.fields import CharField, BooleanField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class Door(Model):
    name = CharField(primary_key=True, max_length=32)

    def is_open(self):
        latest_status = DoorStatus.objects.filter(door=self).order_by('-timestamp').first()
        if latest_status is None:
            return False
        else:
            return latest_status.open

    def open(self):
        DoorStatus.objects.create(open=True, timestamp=timezone.now(), door=self)

    def close(self):
        DoorStatus.objects.create(open=False, timestamp=timezone.now(), door=self)


class DoorStatus(Model):
    open = BooleanField(default=False, null=False, blank=False)
    timestamp = DateTimeField(null=False, blank=False)
    door = ForeignKey(to=Door)
