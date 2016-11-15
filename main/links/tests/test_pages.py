from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from users.models import User


class LinkTests(TestCase):
    fixtures = ['users', 'links']
    site_domain = 'testexample.com'

    def setUp(self):
        '''
        Modify the current site with the
        predefined site domain.
        '''

        site = Site.objects.get_current()
        site.domain = self.site_domain
        site.name = self.site_domain
        site.save()

    def test_index(self):
        '''
        Test the index.
        '''

        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        '''
        Test the dashboard.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        '''
        Test the login page.
        '''

        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        '''
        Test the logout page.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('index')))

    def test_edit_url(self):
        '''
        Test the edit url.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get link.
        link = user.links.first()

        url = reverse('edit-link', kwargs={'key': link.key})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
