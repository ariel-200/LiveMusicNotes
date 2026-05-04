from django.test import TestCase

from django.urls import reverse


class TestHomePage(TestCase):

    def test_home_page_message(self):
        home_page_url = reverse('homepage')
        response = self.client.get(home_page_url)
        self.assertContains(response, 'Welcome to Live Music Notes')


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
