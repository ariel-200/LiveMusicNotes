from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from lmn.models import Artist,Venue,Show,Note


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

class TestNoteModel(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist')
        self.venue = Venue.objects.create(name='Test Venue', city='Minneapolis', state='MN')
        self.user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')

    def test_cannot_create_note_for_future_show(self):
        show = Show.objects.create(artist=self.artist, venue=self.venue, show_date=timezone.now() + timedelta(days=5))
        note = Note(show=show,user=self.user, title='test title', text='test text')
        with self.assertRaises(ValidationError):
            note.full_clean()

