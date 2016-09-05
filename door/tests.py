import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from door.models import Door

TEST_DOOR = 'test'


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


class DoorApiViewTestCase(TestCase):
    def setUp(self):
        door = Door.objects.create(name=TEST_DOOR)

        self.url = reverse('door-api', kwargs={'name': door.name})
        self.factory = RequestFactory()

    def test_get_status_open(self):
        request = self.factory.get(self.url)
        print(request.__dict__)
        print(1, (request.body.decode('utf-8')), 2)

    def test_get_status_closed(self):
        pass

    def test_api_open_without_key(self):
        pass

    def test_api_open_with_wrong_key(self):
        pass

    def test_api_open_with_correct_key(self):
        pass

    def test_api_close_without_key(self):
        pass

    def test_api_close_with_wrong_key(self):
        pass

    def test_api_close_with_correct_key(self):
        pass
