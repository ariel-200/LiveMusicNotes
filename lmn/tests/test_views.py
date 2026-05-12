from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from lmn.models import Artist, Venue, Show, Note


class TestHomePage(TestCase):

    def test_home_page_message(self):
        home_page_url = reverse('homepage')
        response = self.client.get(home_page_url)
        self.assertContains(response, 'Welcome to Live Music Notes')

    def test_homepage_shows_how_to_use_section(self):
        """ Verify homepage shows usage instructions """
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'How to Use')
        self.assertContains(response, 'Visit the Shows page')

    def test_homepage_shows_recent_shows_section(self):
        """ Verify homepage shows recent shows section """
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Recent Shows')

    def test_homepage_shows_latest_notes_section(self):
        """ Verify homepage shows latest notes section """
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Latest Notes')

    def test_homepage_uses_correct_template(self):
        """ Verify homepage uses correct template """
        response = self.client.get(reverse('homepage'))

        self.assertTemplateUsed(response, 'lmn/home.html')


class TestHomepageContent(TestCase):
    """ Tests for homepage recent shows and latest notes content """

    def setUp(self):
        self.artist = Artist.objects.create(name='Homepage Artist')
        self.venue = Venue.objects.create(
            name='Homepage Venue',
            city='Minneapolis',
            state='MN'
        )
        self.user = User.objects.create_user(
            username='homepageuser',
            email='homepageuser@example.com',
            password='password'
        )

    def test_homepage_shows_five_recent_shows(self):
        """ Verify homepage displays only five recent shows """
        for i in range(6):
            Show.objects.create(
                artist=self.artist,
                venue=self.venue,
                show_date=timezone.now() - timedelta(days=i + 1),
                end_date=timezone.now() - timedelta(days=i + 1) + timedelta(hours=2)
            )

        response = self.client.get(reverse('homepage'))

        self.assertEqual(len(response.context['recent_shows']), 5)

    def test_homepage_shows_two_latest_notes(self):
        """ Verify homepage displays only two latest notes """
        for i in range(3):
            show = Show.objects.create(
                artist=self.artist,
                venue=self.venue,
                show_date=timezone.now() - timedelta(days=i + 1),
                end_date=timezone.now() - timedelta(days=i + 1) + timedelta(hours=2)
            )

            Note.objects.create(
                show=show,
                user=self.user,
                title=f'Homepage Note {i}',
                text='This is a homepage note.',
                rating=3
            )

        response = self.client.get(reverse('homepage'))

        self.assertEqual(len(response.context['latest_notes']), 2)

    def test_homepage_displays_recent_show_content(self):
        """ Verify recent show information appears on homepage """
        show = Show.objects.create(
            artist=self.artist,
            venue=self.venue,
            show_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() - timedelta(days=1) + timedelta(hours=2)
        )

        response = self.client.get(reverse('homepage'))

        self.assertContains(response, show.artist.name)
        self.assertContains(response, show.venue.name)

    def test_homepage_displays_latest_note_content(self):
        """ Verify latest note information appears on homepage """
        show = Show.objects.create(
            artist=self.artist,
            venue=self.venue,
            show_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() - timedelta(days=1) + timedelta(hours=2)
        )

        note = Note.objects.create(
            show=show,
            user=self.user,
            title='Homepage Note Title',
            text='This note should appear on the homepage.',
            rating=4
        )

        response = self.client.get(reverse('homepage'))

        self.assertContains(response, note.title)
        self.assertContains(response, note.rating)
        self.assertContains(response, note.text)
        self.assertContains(response, note.user.username)


class TestErrorViews(TestCase):

    def test_404_view(self):
        response = self.client.get('this isnt a url on the site')
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('404.html')

    def test_404_view_object(self):
        # example view that uses the database, get note with pk=10000
        response = self.client.get(reverse('note_detail', kwargs={'note_pk': 10000}))
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('404.html')

    def test_403_view(self):
        # there are no current views that return 403. When users can edit notes, or edit 
        # their profiles, or do other activities when it must be verified that the 
        # correct user is signed in (else 403) then this test can be written.
        pass 
