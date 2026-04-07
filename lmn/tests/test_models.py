from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Show
from django.db import IntegrityError

import datetime

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
    # evaluate show creation conflicts

    def test_create_same_artist_same_venue_same_time_fails():
        pass
    
    def test_create_different_artist_same_venue_same_time_fails():
        pass
    
    def test_create_different_artist_different_venue_same_time():
        pass

    def test_create_different_artist_same_venue_different_time():
        pass

    def test_create_same_artist_different_venue_same_time_fails():
        pass

    def test_create_same_artist_different_venue_different_time():
        pass

    def test_create_same_artist_same_venue_different_time():
        pass

    def test_create_different_artist_different_venue_different_time():
        pass
