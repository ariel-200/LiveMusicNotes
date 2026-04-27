from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta, datetime
from lmn.models import Artist, Venue, Show, Note
from django.core.exceptions import ValidationError


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

    def setUp (self):
        self.artist = Artist.objects.create(name='Test Artist')
        self.venue = Venue.objects.create( name='Test Venue', city='Minneapolis', state='MN')
        self.user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
        self.show = Show.objects.create(artist=self.artist, venue=self.venue, show_date=timezone.now() - timedelta(days=1),
                                        end_date=timezone.now() - timedelta(days=1) + timedelta(hours=1))

    def test_user_cannot_create_two_notes_for_same_show(self):
        Note.objects.create(show=self.show, user=self.user, title='first', text='first note', rating=1)

        with self.assertRaises(IntegrityError):
           Note.objects.create(show=self.show, user=self.user, title='second', text='second note', rating=1)

    def test_cannot_create_note_for_future_show(self):
        show = Show.objects.create(artist=self.artist, venue=self.venue, show_date=timezone.now() + timedelta(days=5), end_date=timezone.now() + timedelta(days=5, hours=2))
        note = Note(show=show,user=self.user, title='test title', text='test text')
        with self.assertRaises(ValidationError):
            note.full_clean()

class TestShow(TestCase):
    # evaluate show creation conflicts

    def setUp(self):  # django jargon
        self.artist1 = Artist.objects.create(name='Jichael Mackson')
        self.artist2 = Artist.objects.create(name='Saylor Twift')

        self.venue1 = Venue.objects.create(name='First Venue', city='Minneapolis', state='MN')
        self.venue2 = Venue.objects.create(name='Second Venue', city='Sacramento', state='CA')

    def test_back_to_back_shows_allowed(self):
        show1 = Show(artist=self.artist1, venue=self.venue1, show_date=datetime(2025, 1, 1, 8, 0), end_date=datetime(2025, 1, 1, 9, 0))
        show1.save()

        show2 = Show(artist=self.artist2, venue=self.venue1, show_date=datetime(2025, 1, 1, 9, 0), end_date=datetime(2025, 1, 1, 10, 0))
        show2.save()  # if error is raised here, test fails

    def test_time_overlap_fails(self):
        show1 = Show(artist=self.artist1, venue=self.venue1, show_date=datetime(2025, 1, 1, 8, 0), end_date=datetime(2025, 1, 1, 9, 0))
        show1.save()

        show2 = Show(artist=self.artist2, venue=self.venue1, show_date=datetime(2025, 1, 1, 8, 30), end_date=datetime(2025, 1, 1, 9, 30))
        with self.assertRaises(ValidationError):
            show2.full_clean()
            show2.save()

    def test_time_nested_fails(self):
        show1 = Show(artist=self.artist1, venue=self.venue1, show_date=datetime(2025, 1, 1, 8, 0), end_date=datetime(2025, 1, 1, 9, 0))
        show1.save()

        show2 = Show(artist=self.artist2, venue=self.venue1, show_date=datetime(2025, 1, 1, 8, 15), end_date=datetime(2025, 1, 1, 8, 45))
        with self.assertRaises(ValidationError):
            show2.full_clean()
            show2.save()

    def test_scheduling_conflicts(self):
        # test every possible artist, venue, time combinations

        start_time1 = datetime(2025, 1, 1, 8, 0)
        end_time1 = datetime(2025, 1, 1, 9, 0)

        start_time2 = datetime(2026, 1, 1, 8, 0)
        end_time2 = datetime(2026, 1, 1, 9, 0)

        # control
        show1 = Show(artist=self.artist1, venue=self.venue1, show_date=start_time1, end_date=end_time1)
        show1.save()

        combinations = [

            # artist       venue        start        end        allowed
            (self.artist1, self.venue1, start_time1, end_time1, False),  # same artist, same venue, same time
            (self.artist2, self.venue2, start_time2, end_time2, True),   # diff artist, diff venue, diff time

            (self.artist1, self.venue2, start_time1, end_time1, True),   # same artist, diff venue, same time
            (self.artist1, self.venue1, start_time2, end_time2, True),   # same artist, same venue, diff time
            (self.artist2, self.venue1, start_time1, end_time1, False),  # diff artist, same venue, same time
            (self.artist2, self.venue2, start_time1, end_time1, True),   # diff artist, diff venue, same time
            (self.artist2, self.venue1, start_time2, end_time2, True),   # diff artist, same venue, diff time
        ]

        for artist, venue, start, end, allowed in combinations:
            with self.subTest(artist=artist, venue=venue, allowed=allowed):
                show2 = Show(artist=artist, venue=venue, show_date=start, end_date=end)

                if not allowed:
                    with self.assertRaises(ValidationError):
                        show2.full_clean()  # need to call bc model validation
                        show2.save()
                elif allowed:
                    show2.save()
                    show2.delete()  # so that next loop does not conflict with this one
