from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from lmn.models import Note, Show, Artist, Venue

from django.utils import timezone
from datetime import timedelta

import datetime
from datetime import timedelta
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import IntegrityError

class TestNoNotesViews(TestCase):

    def test_note_list_with_no_notes_returns_empty_list(self):
        response = self.client.get(reverse('latest_notes'))
        self.assertFalse(response.context['notes'])  # An empty list is false

    def test_add_note_link_shown_for_past_show_when_user_has_no_note(self):
        user= User.objects.create_user(username='testuser', password='testpass1')
        self.client.force_login(user)

        artist= Artist.objects.create(name='Test artist')
        venue= Venue.objects.create(name='Test venue')

        past_show= Show.objects.create(
            artist_id=1,
            venue_id=1,
            show_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=2) + timedelta(hours=2),
        )
        response = self.client.get(reverse('notes_for_show', kwargs={'show_pk': past_show.pk}))

        self.assertContains(response,'Add your own notes for this show')


class TestAddNoteUnauthentictedUser(TestCase):
    # Have to add artists and venues because of foreign key constrains in show
    fixtures = ['testing_artists', 'testing_venues', 'testing_shows'] 

    def test_add_note_unauthenticated_user_redirects_to_login(self):
        response = self.client.get('/notes/add/1/', follow=True)  # Use reverse() if you can, but not required.
        # Should redirect to login; which will then redirect to the notes/add/1 page on success.
        self.assertRedirects(response, '/accounts/login/?next=/notes/add/1/')


class TestAddNotesWhenUserLoggedIn(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):  # Log in the user with pk=1
        user = User.objects.first()
        self.client.force_login(user)

        self.new_show = Show.objects.create( artist_id=1, venue_id=1, show_date=timezone.now() -timedelta(days=1), end_date=timezone.now() - timedelta(days=1) + timedelta(hours=1))

    def test_save_note_for_non_existent_show_is_error(self):
        new_note_url = reverse('new_note', kwargs={'show_pk': 10000})
        response = self.client.post(new_note_url)
        self.assertEqual(response.status_code, 404)

    def test_can_save_new_note_for_show_blank_data_is_error(self):
        initial_note_count = Note.objects.count()

        new_note_url = reverse('new_note', kwargs={'show_pk': self.new_show.pk})

        # No post params
        response=self.client.post(new_note_url, follow=True)
        # No note saved, should show same page
        self.assertTemplateUsed(response,'lmn/notes/new_note.html')

        # no title
        response=self.client.post(new_note_url, {'text': 'blah blah'}, follow=True)
        self.assertTemplateUsed(response,'lmn/notes/new_note.html')

        # no text
        response=self.client.post(new_note_url, {'title': 'blah blah'}, follow=True)
        self.assertTemplateUsed(response,'lmn/notes/new_note.html')

        # nothing added to database
        # 2 test notes provided in fixture, should still be 2
        self.assertEqual(Note.objects.count(), initial_note_count)   

    def test_add_note_database_updated_correctly(self):
        initial_note_count = Note.objects.count()

        new_note_url = reverse('new_note', kwargs={'show_pk': self.new_show.pk})

        self.client.post(
            new_note_url, 
            {'text': 'ok', 'title': 'blah blah', 'rating': 1}, 
            follow=True)

        # Verify note is in database
        new_note_query = Note.objects.filter(text='ok', title='blah blah',show=self.new_show)
        self.assertEqual(new_note_query.count(), 1)

        # And one more note in DB than before
        self.assertEqual(Note.objects.count(), initial_note_count + 1)

        # Date correct? Should be the current date and time. 
        now_timestamp = datetime.datetime.today().timestamp()
        posted_timestamp = new_note_query.first().posted_date.timestamp()

        # Timestamps are to the nearest milisecond and it may take a few seconds
        # to connect and write to the database. So if the test stores now_timestamp, 
        # so the test's now_timestamp will probably be slightly different to the 
        # time stored in the database. 
        # So, we can assert that they are within a few seconds of each other.
        ten_seconds = 10 * 1000
        self.assertAlmostEqual(now_timestamp, posted_timestamp, delta=ten_seconds) 

    def test_redirect_to_note_detail_after_save(self):
        new_note_url = reverse('new_note', kwargs={'show_pk': self.new_show.pk})
        response = self.client.post(
            new_note_url, 
            {'text': 'ok', 'title': 'blah blah', 'rating': 1}, 
            follow=True)

        new_note = Note.objects.filter(user=User.objects.first(), show=self.new_show, text='ok', title='blah blah').first()

        self.assertRedirects(response, reverse('note_detail', kwargs={'note_pk': new_note.pk}))

    def test_user_cannot_add_second_note_for_same_show(self):
     Note.objects.create(show=self.new_show, user=User.objects.first(), title='first', text='first note', rating=1)

     response = self.client.post(
            reverse('new_note', kwargs={'show_pk': self.new_show.pk}), {'title': 'second', 'text': 'second note'})

     self.assertEqual(response.status_code, 400)
     self.assertEqual(Note.objects.filter(user= User.objects.first(), show=self.new_show).count(),1)


class TestNotes(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes'] 

    def test_latest_notes(self):
        response = self.client.get(reverse('latest_notes'))
        # Should be note 3, then 2, then 1
        context = response.context['notes']
        first, second, third = context[0], context[1], context[2]
        self.assertEqual(first.pk, 3)
        self.assertEqual(second.pk, 2)
        self.assertEqual(third.pk, 1)

    def test_notes_for_show_view(self):
        # Verify correct list of notes shown for a Show, most recent first
        # Show 1 has 2 notes with PK = 2 (most recent) and PK = 1
        response = self.client.get(reverse('notes_for_show', kwargs={'show_pk': 1}))
        context = response.context['notes']
        first, second = context[0], context[1]
        self.assertEqual(first.pk, 2)
        self.assertEqual(second.pk, 1)

    def test_notes_for_show_when_show_not_found(self):
        response = self.client.get(reverse('notes_for_show', kwargs={'show_pk': 10000}))
        self.assertEqual(404, response.status_code)

    def test_correct_templates_used_for_notes(self):
        response = self.client.get(reverse('latest_notes'))
        self.assertTemplateUsed(response, 'lmn/notes/note_list.html')

        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 1}))
        self.assertTemplateUsed(response, 'lmn/notes/note_detail.html')
        response = self.client.get(reverse('notes_for_show', kwargs={'show_pk': 1}))
        self.assertTemplateUsed(response, 'lmn/notes/notes_for_show.html')

        # Log someone in, add note
        self.client.force_login(User.objects.first())

        show = Show.objects.create(artist_id=1,venue_id=1,show_date=timezone.now() - timedelta(days=1), end_date=timezone.now() - timedelta(days=1) + timedelta(hours=1))
        response = self.client.get(reverse('new_note', kwargs={'show_pk': show.pk}))
        self.assertTemplateUsed(response, 'lmn/notes/new_note.html')


class TestNoteDetailView(TestCase):
    """ Tests for the note detail page """

    fixtures = ['testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes']

    def test_note_detail_page_loads(self):
        """ Verify note detail page loads successfully """
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 1}))

        self.assertEqual(response.status_code, 200)

    def test_note_detail_uses_correct_template(self):
        """ Verify note detail page uses correct template """
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 1}))

        self.assertTemplateUsed(response, 'lmn/notes/note_detail.html')

    def test_note_detail_shows_show_information(self):
        """ Verify show information appears on note detail page """
        note = Note.objects.get(pk=1)
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': note.pk}))

        self.assertContains(response, note.show.artist.name)
        self.assertContains(response, note.show.venue.name)

    def test_note_detail_shows_note_author(self):
        """ Verify note author appears on note detail page """
        note = Note.objects.get(pk=1)
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': note.pk}))

        self.assertContains(response, note.user.username)

    def test_note_detail_shows_note_title(self):
        """ Verify note title appears on note detail page """
        note = Note.objects.get(pk=1)
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': note.pk}))

        self.assertContains(response, note.title)

    def test_note_detail_shows_note_text(self):
        """ Verify note text appears on note detail page """
        note = Note.objects.get(pk=1)
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': note.pk}))

        self.assertContains(response, note.text)

    def test_note_detail_shows_note_rating(self):
        """ Verify note rating appears on note detail page """
        note = Note.objects.get(pk=1)
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': note.pk}))

        self.assertContains(response, note.rating)

    def test_note_detail_shows_404_for_missing_note(self):
        """ Verify missing note detail page returns 404 """
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 9999}))

        self.assertEqual(response.status_code, 404)


class TestFutureShowRestriction(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_venues']

    def setUp(self):
        self.client.force_login(User.objects.first())


        self.future_show = Show.objects.create(
            artist_id=1,venue_id=1, show_date=timezone.now() +timedelta(days=5),end_date=timezone.now() + timedelta(days=5,hours=2))
    def test_future_show_blocked(self):
            response= self.client.post(reverse('new_note', kwargs={'show_pk':self.future_show.pk}),{'title':'t','text':'t'})
            self.assertEqual(response.status_code,403)

    def test_future_show_get_blocked(self):
                response = self.client.get(
                    reverse('new_note', kwargs={'show_pk': self.future_show.pk})
                )
                self.assertEqual(response.status_code,403)


class TestEditNotes(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes']

    def setUp(self):
        # Logs in as test user prior to running below tests
        self.client.force_login(User.objects.get(username='alice'))

    def test_different_user_attempt_edit(self):
        self.client.force_login(User.objects.get(username='bob'))
        response = self.client.get(reverse('edit_note', kwargs={'note_pk': 1}))
        self.assertEqual(response.status_code, 403)
    
    def test_edit_button_hidden_when_wrong_user(self):
        # Verify non-author cannot see edit button
        # Alice is logged in via setUp, note 2 belongs to bob
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 2}))
        self.assertNotContains(response, 'Edit')
    
    def test_note_prefill_with_form_data(self):
        # Verify note is prefilled with correct information
        # Alice is logged in via setUp and owns note 1 (title='ok', text='kinda ok')
        response = self.client.get(reverse('edit_note', kwargs={'note_pk': 1}))
        self.assertContains(response, 'ok')
        self.assertContains(response, 'kinda ok')

class TestNoteRatings(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_venues', 'testing_shows']

    def setUp(self):
        self.client.force_login(User.objects.first())

    def test_note_rated_less_than_zero_fails(self):
        """
        Note rating should not be below zero
        """
        with self.assertRaises(IntegrityError):  # db constraint?
            Note.objects.create(show_id=1, user=User.objects.first(), title='', text='', rating=-1)

    def test_note_rated_higher_than_five_fails(self):
        """
        Note rating should not be above 5 stars
        """
        with self.assertRaises(ValidationError):
            Note.objects.create(show_id=1, user=User.objects.first(), title='example title', text='example text', rating=6)

    def test_note_rated_null_fails(self):
        """
        Note rating cannot be empty
        """
        with self.assertRaises(IntegrityError):  # db constraint
            Note.objects.create(show_id=1, user=User.objects.first(), title='', text='')
