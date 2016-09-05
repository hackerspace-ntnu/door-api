import json

from django.test import TestCase
from django.test.client import Client
from django.urls.base import reverse

from door.models import Door

TEST_DOOR = 'test'


class JsonClient(Client):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        response.content = json.loads(response.content.decode('utf-8'))
        return response


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
        door.close()
        door.close()

        self.assertEqual(door.doorstatus_set.count(), 1)


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
        self.assertTrue(response.content['open'])

    def test_get_status_closed(self):
        door = Door.objects.get(name=TEST_DOOR)
        door.close()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.content['open'])

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
            'key': 'key',
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
        response = self.client.post(self.url, {
            'open': False,
            'key': 'key',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(door.doorstatus_set.count(), 1)
