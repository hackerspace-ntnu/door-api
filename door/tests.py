import json

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.urls.base import reverse

from door.models import Door
from door.utils import decode_json_bytes

TEST_DOOR = 'test'
DOOR_KEY = 'test-key'


class JsonClient(Client):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        response.decoded_content = decode_json_bytes(response.content)
        return response

    def post(self, path, data=None, *args, **kwargs):
        return super().post(path, data=json.dumps(data), *args, content_type='application/json', **kwargs)


class DoorModelTestCase(TestCase):
    def setUp(self):
        Door.objects.create(name=TEST_DOOR)

    def test_closed_by_default(self):
        door = Door.objects.get(name=TEST_DOOR)

        self.assertFalse(door.is_open())

    def test_is_open(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()

        self.assertTrue(door.is_open())

    def test_has_closed_after_being_open(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        door.close()

        self.assertFalse(door.is_open())

    def test_double_open(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        door.open()

        self.assertEqual(door.doorstatus_set.count(), 1)

    def test_double_close(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        door.close()
        door.close()

        self.assertEqual(door.doorstatus_set.count(), 2)

    def test_statuses_ordering(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        door.close()
        door.open()

        # should be reverse chrono ordered
        t2, t1, t0 = door.doorstatus_set.values_list('timestamp', flat=True)

        self.assertTrue(t2 > t1 > t0)


@override_settings(DOOR_KEY=DOOR_KEY)
class DoorApiViewTestCase(TestCase):
    def setUp(self):
        door = Door.objects.create(name=TEST_DOOR)

        self.url = reverse('door-api', kwargs={'name': door.name})
        self.client = JsonClient()

    def test_get_status_open(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.decoded_content['name'], TEST_DOOR)
        self.assertEqual(response.decoded_content['status']['open'], True)

    def test_get_status_closed(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        door.close()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.decoded_content['status']['open'], False)

    def test_api_open_without_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        response = self.client.post(self.url, {
            'open': True,
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(door.doorstatus_set.count(), 0)

    def test_api_open_with_wrong_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        response = self.client.post(self.url, {
            'open': True,
            'key': 'incorrect key',
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(door.doorstatus_set.count(), 0)

    def test_api_open_with_correct_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        response = self.client.post(self.url, {
            'open': True,
            'key': DOOR_KEY,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(door.doorstatus_set.count(), 1)

    def test_api_close_without_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        response = self.client.post(self.url, {
            'open': False,
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(door.doorstatus_set.count(), 0)

    def test_api_close_with_wrong_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        response = self.client.post(self.url, {
            'open': False,
            'key': 'incorrect key',
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(door.doorstatus_set.count(), 0)

    def test_api_close_with_correct_key(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.open()
        response = self.client.post(self.url, {
            'open': False,
            'key': DOOR_KEY,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(door.doorstatus_set.count(), 2)
