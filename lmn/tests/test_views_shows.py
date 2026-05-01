from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from django.utils import timezone
from datetime import timedelta
from lmn.models import Show, Artist, Venue

class TestShowListView(TestCase):
    """ Tests for the shows page """

    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist')
        self.venue = Venue.objects.create(
            name='Test Venue',
            city='Minneapolis',
            state='MN'
        )

        # Create one past show
        self.past_show = Show.objects.create(
            artist=self.artist,
            venue=self.venue,
            show_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=2) + timedelta(hours=2)
        )

        # Create one upcoming show
        self.upcoming_show = Show.objects.create(
            artist=self.artist,
            venue=self.venue,
            show_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2) + timedelta(hours=2)
        )

    def test_show_list_page_loads(self):
        """ Verify shows page loads successfully """
        response = self.client.get(reverse('show_list'))
        self.assertEqual(response.status_code, 200)

    def test_show_list_uses_correct_template(self):
        """ Verify correct template is used for shows page """
        response = self.client.get(reverse('show_list'))
        self.assertTemplateUsed(response, 'lmn/shows/show_list.html')

    def test_past_and_upcoming_sections_display(self):
        """ Verify past and upcoming show sections appear """
        response = self.client.get(reverse('show_list'))
        self.assertContains(response, 'Past Shows')
        self.assertContains(response, 'Upcoming Shows')

    def test_past_and_upcoming_shows_display(self):
        """ Verify both past and upcoming shows appear on the page """
        response = self.client.get(reverse('show_list'))
        self.assertContains(response, self.past_show.artist.name)
        self.assertContains(response, self.upcoming_show.artist.name)

    def test_shows_are_ordered_correctly(self):
        """ Verify past shows are newest first and upcoming shows are soonest first """
        now = timezone.now()

        venue = Venue.objects.create(
            name='Order Venue',
            city='Minneapolis',
            state='MN'
        )

        # Create artists with unique names for easy ordering checks
        past_old_artist = Artist.objects.create(name='Past Old')
        past_new_artist = Artist.objects.create(name='Past New')
        future_soon_artist = Artist.objects.create(name='Future Soon')
        future_late_artist = Artist.objects.create(name='Future Late')

        # Older past show
        Show.objects.create(
            artist=past_old_artist,
            venue=venue,
            show_date=now - timedelta(days=5),
            end_date=now - timedelta(days=5) + timedelta(hours=2)
        )

        # More recent past show
        Show.objects.create(
            artist=past_new_artist,
            venue=venue,
            show_date=now - timedelta(days=1),
            end_date=now - timedelta(days=1) + timedelta(hours=2)
        )

        # Later upcoming show
        Show.objects.create(
            artist=future_late_artist,
            venue=venue,
            show_date=now + timedelta(days=5),
            end_date=now + timedelta(days=5) + timedelta(hours=2)
        )

        # Sooner upcoming show
        Show.objects.create(
            artist=future_soon_artist,
            venue=venue,
            show_date=now + timedelta(days=1),
            end_date=now + timedelta(days=1) + timedelta(hours=2)
        )

        response = self.client.get(reverse('show_list'))
        content = response.content.decode()

        # Past shows should show most recent first
        self.assertLess(
            content.index('Past New'),
            content.index('Past Old')
        )

        # Upcoming shows should show soonest first
        self.assertLess(
            content.index('Future Soon'),
            content.index('Future Late')
        )

    def test_past_and_upcoming_shows_are_in_correct_context(self):
        """ Verify past and upcoming shows are placed in the correct context """

        response = self.client.get(reverse('show_list'))

        past_shows = response.context['past_shows']
        upcoming_shows = response.context['upcoming_shows']

        # Past show should be in past_shows only
        self.assertIn(self.past_show, past_shows)
        self.assertNotIn(self.past_show, upcoming_shows)

        # Upcoming show should be in upcoming_shows only
        self.assertIn(self.upcoming_show, upcoming_shows)
        self.assertNotIn(self.upcoming_show, past_shows)

    def test_past_show_links_to_notes_page(self):
        """ Verify past shows link to the notes page """
        response = self.client.get(reverse('show_list'))
        self.assertContains(
            response,
            reverse('notes_for_show', kwargs={'show_pk': self.past_show.pk})
        )


class TestCurrentTimeShowView(TestCase):
    """ Tests for shows starting at the current time """

    def setUp(self):
        # Save one fixed point in time for the test
        self.mock_time = timezone.now()

        self.artist = Artist.objects.create(name='Test Artist')
        self.venue = Venue.objects.create(
            name='Test Venue',
            city='Minneapolis',
            state='MN'
        )

        # Create show that starts at the current time
        self.current_show = Show.objects.create(
            artist=self.artist,
            venue=self.venue,
            show_date=self.mock_time,
            end_date=self.mock_time + timedelta(hours=2)
        )

    def test_show_at_current_time_is_past_show(self):
        """ Verify show at current time is included in past shows """
        with patch('lmn.views.views_shows.timezone.now', return_value=self.mock_time):
            response = self.client.get(reverse('show_list'))

            # Get shows sent to the template
            past_shows = response.context['past_shows']
            upcoming_shows = response.context['upcoming_shows']

            # Show should be treated as a past show
            self.assertIn(self.current_show, past_shows)
            self.assertNotIn(self.current_show, upcoming_shows)


class TestShowSearchView(TestCase):
    """ Tests for shows page search functionality """

    def setUp(self):
        self.matching_artist = Artist.objects.create(name='Search Artist')
        self.matching_venue = Venue.objects.create(
            name='Search Venue',
            city='Minneapolis',
            state='MN'
        )

        self.other_artist = Artist.objects.create(name='Other Artist')
        self.other_venue = Venue.objects.create(
            name='Other Venue',
            city='St Paul',
            state='MN'
        )

        # Show that should match artist searches
        self.artist_match_show = Show.objects.create(
            artist=self.matching_artist,
            venue=self.other_venue,
            show_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() - timedelta(days=1) + timedelta(hours=2)
        )

        # Show that should match venue searches
        self.venue_match_show = Show.objects.create(
            artist=self.other_artist,
            venue=self.matching_venue,
            show_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() - timedelta(days=1) + timedelta(hours=2)
        )

        # Show that should not match search
        self.non_matching_show = Show.objects.create(
            artist=self.other_artist,
            venue=self.other_venue,
            show_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=2) + timedelta(hours=2)
        )

    def test_search_finds_artist_name(self):
        """ Verify search finds shows by artist name """
        response = self.client.get(reverse('show_list'), {'search_name': 'Search Artist'})

        self.assertContains(response, self.artist_match_show.artist.name)
        self.assertNotContains(response, self.non_matching_show.artist.name)

    def test_search_finds_venue_name(self):
        """ Verify search finds shows by venue name """
        response = self.client.get(reverse('show_list'), {'search_name': 'Search Venue'})

        self.assertContains(response, self.venue_match_show.venue.name)
        self.assertNotContains(response, self.non_matching_show.venue.name)

    def test_search_is_case_insensitive(self):
        """ Verify search is not case-sensitive """
        response = self.client.get(reverse('show_list'), {'search_name': 'search artist'})

        self.assertContains(response, self.artist_match_show.artist.name)

    def test_search_term_is_sent_to_template(self):
        """ Verify search term is available to the template """
        response = self.client.get(reverse('show_list'), {'search_name': 'Search Artist'})

        self.assertEqual(response.context['search_term'], 'Search Artist')

    def test_empty_search_shows_all_results(self):
        """ Verify empty search does not filter shows """
        response = self.client.get(reverse('show_list'), {'search_name': ''})

        self.assertContains(response, self.artist_match_show.artist.name)
        self.assertContains(response, self.venue_match_show.venue.name)
        self.assertContains(response, self.non_matching_show.artist.name)
