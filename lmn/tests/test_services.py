from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from lmn.models import Note, Show
from lmn.services.spam_filter import is_spam


class TestSpamFilter(TestCase):

    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        self.client.force_login(User.objects.first())
        self.show = Show.objects.create(
            artist_id=1,
            venue_id=1,
            show_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() - timedelta(days=1) + timedelta(hours=1)
        )

    @patch('lmn.services.spam_filter.prompt', return_value='SPAM')
    def test_spam_filter_filters_obvious_spam(self, mock_prompt):
        result = is_spam('Buy cheap concert tickets!!!', 'Click here for deals http://freeconcerttickets.com')
        self.assertTrue(result)

    @patch('lmn.services.spam_filter.prompt', return_value='NOT_SPAM')
    def test_spam_filter_allows_real_message(self, mock_prompt):
        result = is_spam('Awesome concert!', 'The bass guitarist was super tight and the drummer never disapoints!')
        self.assertFalse(result)

    @patch('lmn.services.spam_filter.prompt', return_value='SPAM')
    def test_spam_not_added_to_database(self, mock_prompt):
        initial_count = Note.objects.count()
        self.client.post(
            reverse('new_note', kwargs={'show_pk': self.show.pk}),
            {'title': 'Buy cheap concert tickets!!!', 'text': 'Click here for deals http://freeconcerttickets.com'}
        )
        self.assertEqual(Note.objects.count(), initial_count)

    @patch('lmn.services.spam_filter.prompt', return_value='NOT_SPAM')
    def test_real_message_added_to_database(self, mock_prompt):
        initial_count = Note.objects.count()
        self.client.post(
            reverse('new_note', kwargs={'show_pk': self.show.pk}),
            {'title': 'Great concert!', 'text': 'I really enjoyed this show last night'}
        )
        self.assertEqual(Note.objects.count(), initial_count + 1)