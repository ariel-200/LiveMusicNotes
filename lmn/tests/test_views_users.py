from django.test import TestCase

from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate

from django.contrib.auth.models import User, AnonymousUser
from lmn.models import Note


class TestUserProfile(TestCase):
    # Have to add artists and venues because of foreign key constrains in show
    fixtures = ['testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes'] 

    # verify correct list of reviews for a user
    def test_user_profile_show_list_of_their_notes(self):
        # get user profile for user 2. Should have 2 reviews for show 1 and 2.
        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 2}))
        notes_expected = list(Note.objects.filter(user=2).order_by('-posted_date'))
        notes_provided = list(response.context['notes'])
        self.assertTemplateUsed('lmn/users/user_profile.html')
        self.assertEqual(notes_expected, notes_provided)

        # test notes are in date order, most recent first.
        # Note PK 3 should be first, then PK 2
        first_note = response.context['notes'][0]
        self.assertEqual(first_note.pk, 3)

        second_note = response.context['notes'][1]
        self.assertEqual(second_note.pk, 2)

    def test_user_with_no_notes(self):
        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 3}))
        self.assertFalse(response.context['notes'])

    def test_username_shown_on_profile_page(self):
        # A string "username's notes" is visible
        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 1}))
        self.assertContains(response, 'alice\'s notes')

        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 2}))
        self.assertContains(response, 'bob\'s notes')

    def test_correct_user_name_shown_different_profiles(self):
        logged_in_user = User.objects.get(pk=2)
        self.client.force_login(logged_in_user)  # bob
        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 2}))
        self.assertContains(response, 'You are logged in, <a href="/user/profile/2/">bob</a>.')

        # Same message on another user's profile. Should still see logged in message 
        # for currently logged in user, in this case, bob
        response = self.client.get(reverse('user_profile', kwargs={'user_pk': 3}))
        self.assertContains(response, 'You are logged in, <a href="/user/profile/2/">bob</a>.')


class TestUserAuthentication(TestCase):
    """ Some aspects of registration (e.g. missing data, duplicate username) covered in test_forms """
    """ Currently using much of Django's built-in login and registration system """

    def test_user_registration_logs_user_in(self):
        self.client.post(
            reverse('register'), 
            {
                'username': 'sam12345', 
                'email': 'sam@sam.com', 
                'password1': 'feRpj4w4pso3az', 
                'password2': 'feRpj4w4pso3az', 
                'first_name': 'sam', 
                'last_name': 'sam'
            }, 
            follow=True)

        # Assert user is logged in - one way to do it...
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'sam12345')

        # This works too. Don't need both tests, added this one for reference.
        # sam12345 = User.objects.filter(username='sam12345').first()
        # auth_user_id = int(self.client.session['_auth_user_id'])
        # self.assertEqual(auth_user_id, sam12345.pk)

    def test_user_registration_redirects_to_correct_page(self):
        # TODO If user is browsing site, then registers, once they have registered, they should
        # be redirected to the last page they were at, not the homepage.
        response = self.client.post(
            reverse('register'), 
            {
                'username': 'sam12345', 
                'email': 'sam@sam.com', 
                'password1': 'feRpj4w4pso3az@1!2', 
                'password2': 'feRpj4w4pso3az@1!2', 
                'first_name': 'sam', 
                'last_name': 'sam'
            }, 
            follow=True)
        new_user = authenticate(username='sam12345', password='feRpj4w4pso3az@1!2')
        self.assertRedirects(response, reverse('user_profile', kwargs={"user_pk": new_user.pk}))   
        self.assertContains(response, 'sam12345')  # page has user's username on it


class Logout(TestCase):

    fixtures = ['testing_users']

    def test_logout_link_logs_out(self):
        logged_in_user = User.objects.get(pk=2)
        self.client.force_login(logged_in_user) 

        logout = reverse('logout')
        response = self.client.post(logout)
        logged_in_user = auth.get_user(self.client)
        self.assertIsInstance(logged_in_user, AnonymousUser)


    def test_logout_redirects_home(self):
        logged_in_user = User.objects.get(pk=2)
        self.client.force_login(logged_in_user) 

        logout = reverse('logout')
        response = self.client.post(logout, follow=True)
        self.assertTemplateUsed('home.html')
