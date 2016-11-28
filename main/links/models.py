import random
import re

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Link(models.Model):
    '''
    Basic Link.
    '''

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(
        'Tag',
        related_name='links',
        verbose_name='Link Tags',
        help_text='The tags of the link',
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Link Title',
        help_text='The title of this link',
        blank=True
    )

    destination = models.URLField(
        max_length=300,
        verbose_name='Destination Url',
        help_text='The destination url'
    )

    key = models.CharField(
        max_length=80,
        verbose_name='Key',
        help_text='The unique identifier for the link'
    )

    user = models.ForeignKey(
        'users.User',
        related_name='links',
        verbose_name='User',
        help_text='The creator of the link',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{} - {}'.format(self.key, self.destination[:20])

    def add_unique_ip(self, ip_address=None):
        '''
        Update Unique IP Address for the Link.
        '''
        if ip_address:
            self.addresses.update_or_create(address=ip_address)

    @property
    def total_clicks(self):
        '''
        Return sum of all region's total clicks.
        '''
        sum_data = self.regions.aggregate(Sum('total_clicks'))
        return sum_data['total_link_sum']

    @property
    def unique_clicks(self):
        '''
        Return the total number of unique addresses that visited the Link.
        '''
        return self.addresses.count()

    @staticmethod
    def _generate_key():
        '''
        Generate a random string based on the Hash length and Alphabet.
        '''

        return ''.join(
            random.choice(settings.HASH_ALPHABET)
            for x in range(settings.HASH_LENGTH)
        )

    @classmethod
    def make_key(cls):
        '''
        Make random key for Link.
        Ensure uniqueness of key by querying Database.
        '''

        key = cls._generate_key()
        while cls.objects.filter(key=key).exists():
            key = cls._generate_key()
        return key

    @classmethod
    def normalize_key(cls, text):
        '''
        Keys may only contain alphanumberic characters and dashes.
        '''

        key_text = re.match(r'^[A-Za-z0-9-]+$', text)
        if key_text:
            key_text = key_text.string
        else:
            return None

        # Replace all dashes left and right of the string.
        key_text = (
            key_text
            .lstrip('-')
            .rstrip('-')
        )

        # Substitute 2 or more dashes with 1 dash.
        key_text = re.sub(r'-{2,}', '-', key_text)

        return key_text if key_text else None

    class Meta:
        ordering = ('created_on',)


class Tag(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Tag Name',
        help_text='Name of tag',
    )

    def __str__(self):
        return self.name

    @classmethod
    def normalize_text(cls, text):
        # Match text with regular expression to make sure
        # string contains only alphanumberic or '-' characters.
        tag_text = re.match(r'^[A-Za-z0-9\s-]+$', text)

        # If tag text is a <re Match> object, use
        # matched string, else return None.
        if tag_text:
            tag_text = tag_text.string
        else:
            return None

        # Lower all characters.
        # Remove all whitespaces left and right of string.
        # Replace whitespaces with '-'.
        tag_text = (
            text
            .lower()
            .lstrip()
            .rstrip()
        )

        # Substitute 2 or more whitespaces with 1 whitespace.
        tag_text = re.sub(r'\s{2,}', ' ', tag_text)

        # Replace whitespaces with dashes.
        tag_text = tag_text.replace(' ', '-')

        # Substitute 2 or more dashes with 1 dash.
        tag_text = re.sub(r'-{2,}', '-', tag_text)

        # Replace all dashes left and right of the string.
        tag_text = (
            tag_text
            .lstrip('-')
            .rstrip('-')
        )

        return tag_text

    class Meta:
        ordering = ('name',)
