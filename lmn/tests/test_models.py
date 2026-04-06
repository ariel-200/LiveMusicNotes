from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

class TestShow(TestCase):

    def test_create_show_same_venue_same_time_fails(self):
        # make sure that creating 2 different shows at the same time at the same venue location fails
        # validation error
        pass

    def test_create_show_same_venue_overlap_time_fails(self):
        # make sure that creating 2 different shows at the overlapping times at the same venue location fails
        # validation error

        pass
    def test_create_show_different_venue_same_time_same_artist_fails(self):
        # make sure that creating 2 different shows with the same artist performing at the same time at different venues is not possible
        # validation error
        pass

    def test_create_second_show_starting_at_the_end_of_first(self):
        # should be able to create shows that start at the exact end time of a previous show at the same venue
        pass

    def test_create_show_different_venue_same_time(self):
        # should be able to create a show that is at the same time but different venue locations
        pass

    def test_create_show_different_venue_overlapping_time(self):
        # should be able to create a show that is at overlapping times with a different show but different venue locations
        pass
