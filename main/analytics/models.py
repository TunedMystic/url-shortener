from django.db import models
from django.utils import timezone

from links.models import Link


class Referer(models.Model):
    link = models.ForeignKey(
        Link,
        related_name='referers',
        verbose_name='Referer',
        help_text="A link's referer",
        on_delete=models.CASCADE
    )

    source = models.CharField(
        max_length=80,
        verbose_name='Referer source',
        help_text='The referer for the link',
        blank=True
    )

    clicks = models.PositiveIntegerField(
        default=0,
        verbose_name='Total referer clicks',
        help_text='The total clicks from this referer'
    )

    last_visited = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
