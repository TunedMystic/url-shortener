import random

from django.conf import settings
from django.db import models
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
        null=True
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

    total_clicks = models.PositiveIntegerField(
        default=0,
        verbose_name='Total clicks',
        help_text='The total clicks on this link'
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
        tag_text = (
            text
            .lower()
            .lstrip()
            .rstrip()
            .replace(' ', '-')
        )
        # If tag text is normalized to an empty
        # string, return None instead.
        return tag_text or None

    class Meta:
        ordering = ('name',)
