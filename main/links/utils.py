from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.sites.models import Site
from django.db.models import F
from django.utils import timezone

import geoip2

from analytics.models import Country, Referer, Region


def update_link_unique_ips(link, ip_address=None):
    '''
    Update Unique IP addresses for Link.
    '''

    link.add_unique_ip(ip_address)


def update_link_regions(link, ip_address=None):
    '''
    Create or Update Region objects for Link.
    '''

    # Initialize GeoIP object.
    g = GeoIP2()
    country = None

    # Attempt to get country for ip address.
    try:
        data = g.country(ip_address)
        country = data.get('country_name')
        code = data.get('country_code')

        # Get or create country if country does not exist.
        if country:
            country, created = Country.objects.get_or_create(
                name=country,
                code=code
            )

    except (TypeError, geoip2.errors.AddressNotFoundError):
        # Ignore the cases where `ip_address` is None, or
        # the ip address does not exist in the GeoIP2 database.
        pass

    # Get or create Region object, where country is either an object or None.
    region, created = Region.objects.get_or_create(link=link, country=country)

    # Update last visited, clicks, and save changes.
    region.last_visited = timezone.now()
    region.total_clicks = F('total_clicks') + 1
    region.save()


def update_link_referers(link, referer_source=None):
    '''
    Create or Update Referer objects for Link.
    '''

    # If referer exists, normalize.
    if referer_source:
        referer_source = Referer.normalize_source(referer_source)
        if referer_source == Site.objects.get_current().domain:
            referer_source = ''

    # Get or create Referer object.
    referer, created = Referer.objects.get_or_create(
        link=link,
        source=referer_source
    )

    # Update last visited, clicks, and save changes.
    referer.last_visited = timezone.now()
    referer.total_clicks = F('total_clicks') + 1
    referer.save()
