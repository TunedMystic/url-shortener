from django.test import TestCase
from django.contrib.sites.models import Site

from users.models import User
from links.forms import LinkForm, LinkEditForm
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

    def test_remove_stale_links_1(self):
        '''
        Attempt to edit a link with LinkEditForm
        with authenticated user.

        Add a newly created tag to a link.
          - Check tag to see link relations.
          - Check that tag exists in link's tags.
        Remove the tag.
          - Check that tag is removed from link's tags.
          - Check that tag is completely deleted.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get a link created by user.
        link1 = Link.objects.filter(user=user).first()

        # Create a tag.
        tag1 = Tag.objects.create(name='test-tag-1')

        # link1's data for LinkEditForm.
        d = {
            'destination': link1.destination,
            'title': link1.title,
            'tags': tag1.name
        }

        # Edit link1 to 'add' tag1.
        form = LinkEditForm(d, instance=link1, user=user)

        # Before saving form, check that tag1 has no links relations.
        self.assertFalse(tag1.links.exists())

        # Ensure that the Link form is valid and save it.
        self.assertEqual(form.is_valid(), True)
        link = form.save()

        # Check that tag1 is in link's tag set.
        self.assertIn(tag1, link.tags.all())
        # Check that tag1 has 1 link relations.
        self.assertTrue(tag1.links.exists())
        self.assertEqual(tag1.links.count(), 1)

        # Edit data to remove tag from Link1's data.
        d['tags'] = ''

        # Edit link1 to remove tag1.
        form = LinkEditForm(d, instance=link1, user=user)

        # Ensure that the Link form is valid and save it.
        self.assertEqual(form.is_valid(), True)
        link = form.save()

        # Check that tag1 is NOT in link's tag set.
        self.assertFalse(tag1 in link.tags.all())
        # Check that tag1 no longer exists.
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(name=tag1.name).exists()

    def remove_stale_links_2(self):
        '''
        Attempt to edit two links with LinkEditForm
        with authenticated user.

        Add a newly created tag to two links, link1 and link2.
          - Check tag to see link relations.
          - Check that tag exists in each link's tags.
        Remove the tag from one link, link2.
          - Check that tag is removed from link2's tags.
          - Check that tag still exists in link1's tags.
          - Check that tag still exists.
        '''

        # Get the User and Login the User.
        user = User.objects.get(email='user@email.com')
        self.client.login(email=user.email, password='user')

        # Get two links created by user.
        link1, link2 = Link.objects.filter(user=user)[:2]

        # Create a tag.
        tag1 = Tag.objects.create(name='test-tag-1')

        # link1's data for LinkEditForm.
        d1 = {
            'destination': link2.destination,
            'title': link2.title,
            'tags': tag1.name
        }

        # link2's data for LinkEditForm.
        d2 = {
            'destination': link2.destination,
            'title': link2.title,
            'tags': tag1.name
        }

        # Edit link1 and link2 to 'add' tag1.
        form1 = LinkEditForm(d1, instance=link1, user=user)
        form2 = LinkEditForm(d2, instance=link2, user=user)

        # Ensure that both forms are valid, save them.
        self.assertTrue(form1.is_valid())
        self.assertTrue(form2.is_valid())
        link1_edited = form1.save()
        link2_edited = form2.save()

        # Check tag1 is in link1 and link2's tags.
        self.assertIn(tag1, link1_edited.tags.all())
        self.assertIn(tag1, link2_edited.tags.all())
        # Check that tag1 has 2 link relations.
        self.assertTrue(tag1.links.exists())
        self.assertEqual(tag1.links.count(), 2)

        # Edit data to remove tag from link2's data.
        d2['tags'] = ''

        # Edit link2 to remove tag1.
        form2a = LinkEditForm(d2, instance=link2, user=user)

        # Ensure form is valid, save it.
        self.assertTrue(form2a.is_valid())
        link2_edited2 = form2a.save()

        # Check that tag1 is removed from link2's tags.
        self.assertFalse(tag1 in link2_edited2.tags.all())
        # Check that tag2 is still in link1's tags.
        self.assertTrue(tag1 in link1.tags.all())
        # Check that tag still exists.
        self.assertTrue(Tag.objects.get(name=tag1.name).exists())
