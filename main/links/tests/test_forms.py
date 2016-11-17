from django.test import TestCase
from django.contrib.sites.models import Site

from users.models import User
from links.forms import LinkForm, LinkEditForm
from links.models import Link


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

    def test_link_form_anon(self):
        '''
        Create VALID short url with LinkForm
        with unauthenticated user.
        '''

        # Instantiate LinkForm.
        form = LinkForm({
            'destination': 'http://example1.com'
        })

        # Ensure that the link form is valid and save it.
        self.assertEqual(form.is_valid(), True)
        link = form.save()

        # Ensure that the link has no associated User.
        self.assertEqual(link.user, None)

        # Create INVALID short url.
        invalid_key = link.key
        form = LinkForm({
            'destination': 'http://website1.com',
            'key': invalid_key
        })

        # Ensure that the link form is invalid. In this case, the key
        # should already exist in the database and therefore raise an error.
        self.assertEqual(form.is_valid(), False)

    def test_link_form_user(self):
        '''
        Create VALID short url with LinkForm
        with an authenticated user.
        '''

        # Get a user and instantiate LinkForm with user.
        user = User.objects.first()
        form = LinkForm({
            'destination': 'http://example2.com'
        }, user=user)

        # Ensure that the Link form is valid and save it.
        self.assertEqual(form.is_valid(), True)
        link = form.save()

        # Ensure that the Link has an associated User.
        self.assertEqual(link.user, user)

    def test_link_edit_anon(self):
        '''
        Attempt to edit a link with LinkEditForm
        with unauthenticated user.

        Fields edited are title, destination, and tags.
        '''

        # Get a link that has no User.
        some_link = Link.objects.filter(user=None).first()
        form = LinkEditForm({
            'destination': 'http://example3.com',
            'title': 'example 3',
            'tags': 'example-3, example_3'
        }, instance=some_link)

        # Assert that Link Edit form is invalid.
        self.assertEqual(form.is_valid(), False)

    def test_link_edit_auth(self):
        '''
        Attempt to edit a link with LinkEditForm
        with authenticated user.

        Fields edited are title, destination, and tags.

        (Edit tags by adding an invalid and valid tag.
        Test that only valid tag was saved.)
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link that was created by user.
        some_link = Link.objects.filter(user=user).first()

        # Store link's destination and title for reference.
        destination = some_link.destination
        title = some_link.title
        # Clear link's tags.
        some_link.tags.clear()

        # Instantiate Link Edit Form with data, instance, user.
        form = LinkEditForm({
            'destination': 'http://example4.com',
            'title': 'example 4',
            'tags': 'example-4, new_example&*'
        }, instance=some_link, user=user)

        # Ensure that the Link form is valid and save it.
        self.assertEqual(form.is_valid(), True)
        link = form.save()

        # Assert that link's destination and title have been changed.
        self.assertNotEqual(destination, link.destination)
        self.assertNotEqual(title, link.title)
        # Assert that one Tag created.
        self.assertEqual(link.tags.count(), 1)

        # Assert that user is still same.
        self.assertEqual(link.user, user)
