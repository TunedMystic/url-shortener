from django.db import models

from links.models import Link


class IPAddress(models.Model):
    '''
    The IPAddress model will hold ip address information for a link.
    Collectively, all IPAddress relations for a Link will be unique.
    '''

    link = models.ForeignKey(
        Link,
        related_name='addresses',
        on_delete=models.CASCADE
    )

    address = models.GenericIPAddressField()

    def __str__(self):
        return self.address
