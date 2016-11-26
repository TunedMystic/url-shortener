from urllib.parse import urlparse

from django.db import models
from django.utils import timezone

from links.models import Link


class IPAddress(models.Model):
    '''
    The IPAddress model will hold ip address information for a link.
    Collectively, all IPAddress relations for a Link will be unique.
    '''

    link = models.ForeignKey(
        Link,
        related_name='addresses',
        verbose_name='Link',
        on_delete=models.CASCADE
    )

    address = models.GenericIPAddressField()

    def __str__(self):
        return self.address


class Referer(models.Model):
    link = models.ForeignKey(
        Link,
        related_name='referers',
        verbose_name='Link',
        on_delete=models.CASCADE
    )

    source = models.CharField(
        max_length=80,
        verbose_name='Referer source',
        help_text='The source of the referer',
        blank=True
    )

    total_clicks = models.PositiveIntegerField(
        default=0,
        verbose_name='Total referer clicks',
        help_text='The total clicks for this referer'
    )

    last_visited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.source

    @staticmethod
    def normalize_source(url):
        '''
        Return hostname (including subdomains) of url.
        '''
        url = urlparse(url)
        return url.hostname or url.path
