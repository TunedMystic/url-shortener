from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from users.models import User
from links.models import Link, Tag


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

    def test_guest_link_post(self):
        '''
        Test the 'shorten-link' endpoint with VALID
        data from a guest User.
        '''

        url = reverse('shorten-link')

        # Prepare data and POST it.
        data = {'destination': 'http://website2.com'}
        response = self.client.post(url, data=data)

        # Check the response status code and response data.
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('url', response_data)

        link = Link.objects.get(key=response_data.get('url'))
        # Check that the Link has no associated User.
        self.assertEqual(link.user, None)

    def test_user_link_post(self):
        '''
        Test the 'shorten-link' endpoint with VALID
        data from a logged in User.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        url = reverse('shorten-link')

        # Prepare data and POST it.
        data = {'destination': 'http://website3.com'}
        response = self.client.post(url, data=data)

        # Check the response status code and response data.
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('url', response_data)

        link = Link.objects.get(key=response_data.get('url'))
        # Check that the Link has an associated User.
        self.assertEqual(link.user, user)

    def test_domain_link(self):
        '''
        Test the 'shorten-link' endpoint with a url
        that has this site's domain.

        This test should fail with a 400 error.
        '''

        url = reverse('shorten-link')

        # Prepare data and POST it.
        data = {'destination': 'http://{}'.format(self.site_domain)}
        response = self.client.post(url, data=data)

        # Check the response status code.
        self.assertEqual(response.status_code, 400)

    def test_anon_link_key(self):
        '''
        Test the 'shorten-link' endpoint with
        a destination and key provided by an anonymous user.

        This test should fail with a 400 error.
        '''

        url = reverse('shorten-link')

        # Prepare data and POST it.
        data = {'destination': 'http://website4.com', 'key': 'w4'}
        response = self.client.post(url, data=data)

        # Check the response status code.
        self.assertEqual(response.status_code, 400)

    def test_user_existing_key(self):
        '''
        Test the 'shorten-link' endpoint with
        an existing key provided by a logged in user.

        This test should fail with a 400 error.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        url = reverse('shorten-link')
        key = 'w4'

        # Prepare data and POST it.
        data = {'destination': 'http://website4.com', 'key': key}
        response = self.client.post(url, data=data)

        # Check the response status code and response data.
        self.assertEqual(response.status_code, 200)

        # Prepare data with previous key and POST it.
        data = {'destination': 'http://mysite4.com', 'key': key}
        response = self.client.post(url, data=data)

        # Check the response status code.
        self.assertEqual(response.status_code, 400)

    def test_redirect_status_code(self):
        '''
        Test the 'redirect-to-link' endpoint for 301 status code
        and cache control header.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Shorten a url
        url = reverse('shorten-link')
        key = 'w5'

        # Prepare data and POST it.
        data = {'destination': 'http://website5.com', 'key': key}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

        # Prepare redirect url and GET it.
        url = reverse('redirect-to-link', kwargs={'key': key})
        response = self.client.get(url)

        # Check the response status code and headers.
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.has_header('Cache-Control'))
        self.assertTrue(response.has_header('Location'))

    def test_edit_link_anon(self):
        '''
        Test the 'edit-link' endpoint with
        an unauthorized user.
        '''

        # Get a link that has no user and reverse url.
        some_link = Link.objects.filter(user=None).first()
        key = some_link.key
        url = reverse('edit-link', kwargs={'key': key})

        # Prepare data and POST it.
        data = {
            'destination': 'http://website6.com',
            'title': 'website 6',
            'tags': 'website-6'
        }
        response = self.client.post(url, data=data)

        # Check response status code.
        # Should redirect to 'login' page.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_edit_link_auth(self):
        '''
        Test the 'edit-link' endpoint with
        an authorized user.

        Fields edited are title, destination, and tags.

        (Edit tags by adding an invalid and valid tag.
        Test that only valid tag was saved.)
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link that was created by user.
        some_link = Link.objects.filter(user=user).first()
        key = some_link.key
        url = reverse('edit-link', kwargs={'key': key})
        # Clear link's tags.
        some_link.tags.clear()

        # Prepare data and POST it.
        data = {
            'destination': 'http://website7.com',
            'title': 'website 7',
            'tags': 'website-7, *7th_website*'
        }
        response = self.client.post(url, data=data)

        # Get updated link and assert that one Tag created.
        updated_link = Link.objects.get(pk=some_link.pk)
        self.assertEqual(updated_link.tags.count(), 1)

        # Check response status code.
        # Should redirect to 'dashboard' page.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('dashboard')))

    def test_edit_forbidden_link_auth(self):
        '''
        Test the 'edit-link' endpoint with
        an authorized user, trying to edit
        another authorized user's link.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link that was not created by user and user not None.
        some_link = Link.objects.exclude(user=user).exclude(user=None).first()
        self.assertNotEqual(user, some_link.user)

        # Get link's key and reverse url.
        key = some_link.key
        url = reverse('edit-link', kwargs={'key': key})

        # Prepare data and POST it.
        data = {
            'destination': 'http://website8.com',
            'title': 'website 8',
            'tags': 'website-8, web_8'
        }
        response = self.client.post(url, data=data)

        # Check response status.
        self.assertEqual(response.status_code, 403)

    def test_edit_create_and_remove_tags_auth(self):
        '''
        Test the 'edit-link' endpoint with
        an authorized user, trying to remove all
        tags and save link.
        '''

        # Get the User and Login the User
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link that was created by user.
        some_link = Link.objects.filter(user=user).first()
        key = some_link.key
        url = reverse('edit-link', kwargs={'key': key})
        # Clear link's tags.
        some_link.tags.clear()

        # Prepare data and POST it.
        data = {
            'destination': 'http://website9.com',
            'title': 'website 9',
            'tags': 'website-9, *9th_website*, website-nine'
        }
        response = self.client.post(url, data=data)

        # Get updated link and assert that one Tag created.
        updated_link = Link.objects.get(pk=some_link.pk)
        self.assertEqual(updated_link.tags.count(), 2)

        # Check response status code.
        # Should redirect to 'dashboard' page.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('dashboard')))

        # Remove tags from data and post.
        data['tags'] = ''
        response = self.client.post(url, data=data)

        # Get updated link and assert that one Tag created.
        updated_link = Link.objects.get(pk=some_link.pk)
        self.assertEqual(updated_link.tags.count(), 0)

        # Check response status code.
        # Should redirect to 'dashboard' page.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('dashboard')))

    def test_edit_tags_limit(self):
        '''
        Test the 'edit-link' endpoint with
        an authorized user, trying to add more
        than tag limit.
        '''

        # Get the tag_limit from settings.
        from django.conf import settings
        tag_limit = settings.TAG_LIMIT

        # Get the User and Login the User
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link that was created by user.
        some_link = Link.objects.filter(user=user).first()
        key = some_link.key
        url = reverse('edit-link', kwargs={'key': key})
        # Clear link's tags.
        some_link.tags.clear()

        # Generate tags.
        tags = ''
        for i in range(tag_limit+1):
            tags += 'tag {},'.format(i+1)

        # Prepare data and POST it.
        data = {
            'destination': 'http://website10.com',
            'title': 'website 10',
            'tags': tags
        }

        response = self.client.post(url, data=data)

        # Get updated link and assert that one Tag created.
        updated_link = Link.objects.get(pk=some_link.pk)
        self.assertEqual(updated_link.tags.count(), 0)

        # Check response status and response text to see if
        # error was displayed.
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Cannot have more than {} tags.'.format(tag_limit),
            1, 200)
