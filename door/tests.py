from django.test import TestCase

from door.models import Door

TEST_DOOR = 'TEST_DOOR'


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
