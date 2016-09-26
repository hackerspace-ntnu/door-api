from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class Door(Model):
    name = CharField(primary_key=True, max_length=32)

    @property
    def latest_status(self):
        return self.doorstatus_set.first()

    def is_open(self):
        latest_status = self.latest_status

        if latest_status is None:
            return False
        else:
            return latest_status.open

    def open(self):
        if self.is_open():
            return False

        DoorStatus.objects.create(open=True, timestamp=timezone.now(), door=self)
        return True

    def close(self):
        if not self.is_open():
            return False

        DoorStatus.objects.create(open=False, timestamp=timezone.now(), door=self)
        return True

    def get_status_dict(self):
        """
        Returns a dict representation that can be json dumped
        """
        latest_status = self.latest_status

        return {
            'name': self.name,
            'status': self.latest_status.get_status_dict(),
        }

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class DoorStatus(Model):
    open = BooleanField(default=False, null=False, blank=False)
    timestamp = DateTimeField(null=False, blank=False)
    door = ForeignKey(to=Door)

    def get_status_dict(self):
        """
        Returns a dict representation that can be json dumped
        """
        return {
            'open': self.open,
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self):
        return '{name} {timestamp} {status}'.format(
            name=self.door.name,
            timestamp=self.timestamp,
            status='OPEN' if self.open else 'CLOSED',
        )

    class Meta:
        ordering = ('door', '-timestamp',)
