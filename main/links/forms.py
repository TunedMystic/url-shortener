from urllib.parse import urlparse

from django import forms
from django.contrib.sites.models import Site

from .models import Link


class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['key'].required = False

    def clean_key(self):
        '''
        Raise validation if key is given, but User is not given.
        Raise validation if user enters an existing key.
        '''
        user_not_exists = not self.user or not self.user.is_authenticated
        key = self.cleaned_data.get('key')

        # If key is given and (user is None or
        # user not authenticated), raise exception.
        if key and user_not_exists:
            raise forms.ValidationError('Only logged in users can define key.')

        # If a key is given and an existing url has same key, raise exception.
        if key and Link.objects.filter(key=key).exists():
            raise forms.ValidationError('Custom link is already taken!')
        return key

    def clean_destination(self):
        '''
        Raise validation if user enters a url that originates from this site.
        '''
        destination = self.cleaned_data.get('destination')
        url = urlparse(destination)
        site_domain = Site.objects.get_current().domain

        if url.hostname == site_domain:
            raise forms.ValidationError('Sorry, this url is not allowed!')

        return destination

    def clean(self, *args, **kwargs):
        cleaned_data = super(LinkForm, self).clean(*args, **kwargs)
        return cleaned_data

    def save(self, commit=True):
        '''
        Overrides LinkForm.save().
        Generates key if key does not exist.
        Sets user if user is authenticated.
        '''
        link = super(LinkForm, self).save(commit=False)

        # Generate random key for Link if key does not exist.
        if not link.key:
            link.key = Link.make_key()

        # Set user if user is authenticated.
        if self.user and self.user.is_authenticated:
            link.user = self.user

        link.save()
        return link

    class Meta:
        model = Link
        fields = ['destination', 'key']
