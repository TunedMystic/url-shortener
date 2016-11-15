from urllib.parse import urlparse

from django import forms
from django.contrib.sites.models import Site

from .models import Link


class LinkFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LinkFormMixin, self).__init__(*args, **kwargs)
        key_field = self.fields.get('key')
        if key_field:
            key_field.required = False

    def clean_destination(self):
        '''
        Raise validation if User enters a url that originates from this site.
        '''
        destination = self.cleaned_data.get('destination')
        url = urlparse(destination)
        site_domain = Site.objects.get_current().domain

        if url.hostname == site_domain:
            raise forms.ValidationError('Sorry, this url is not allowed!')

        return destination

    def clean_key(self):
        '''
        Raise validation if key is given, but User is not given.
        Raise validation if User enters an existing key.
        '''
        user_not_exists = not self.user or not self.user.is_authenticated
        key = self.cleaned_data.get('key')

        # If key is given and (User is None or
        # User not authenticated), raise exception.
        if key and user_not_exists:
            raise forms.ValidationError('Only logged in users can define key.')

        # If a key is given and an existing url has same key, raise exception.
        if key and Link.objects.filter(key=key).exists():
            raise forms.ValidationError('Custom link is already taken!')
        return key

    def clean_title(self):
        '''
        Raise validation if title is given, but User is not given.
        '''
        user_not_exists = not self.user or not self.user.is_authenticated
        title = self.cleaned_data.get('title')

        # If title is given and (User is None or
        # User not authenticated), raise exception.
        if title and user_not_exists:
            raise forms.ValidationError(
                'Only logged in users can define a title.'
            )
        return title

    def save(self, commit=True):
        '''
        Overrides form save method.
        Generates key if key does not exist.
        Sets User if user is authenticated.
        '''
        link = super(LinkFormMixin, self).save(commit=False)

        # Generate random key for Link if key does not exist.
        if not link.key:
            link.key = Link.make_key()

        # Set User if User is authenticated.
        if self.user and self.user.is_authenticated:
            link.user = self.user

        # Set default link title
        if not link.title:
            title = 'Link - {}'.format(link.key)
            link.title = title

        link.save()
        return link


class LinkForm(LinkFormMixin, forms.ModelForm):
    class Meta:
        model = Link
        fields = ['destination', 'key']


class LinkEditForm(LinkFormMixin, forms.ModelForm):
    class Meta:
        model = Link
        fields = ['destination', 'title']
