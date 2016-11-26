import gzip
import os
import shutil
import urllib

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Download the geolite binaries and store in GEOIP_PATH'

    def download_and_extract_file(self, item):
        filename = item.get('filename')

        # Download file.
        urllib.request.urlretrieve(item.get('location'), filename)

        # Extract file.
        with gzip.open(filename, 'rb') as gzip_file:
            file_data = gzip_file.read()

            with open(item.get('extract_name'), 'wb') as f:
                f.write(file_data)

        self.stdout.write(self.style.SUCCESS('Downloaded and extracted \'{}\''.format(filename)))

    def handle(self, *args, **options):
        path = settings.GEOIP_PATH

        files = [
            {
                'location': 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz',
                'filename': os.path.join(path, 'GeoLite2-Country.mmdb.gz'),
                'extract_name': os.path.join(path, 'GeoLite2-Country.mmdb'),
            },
            {
                'location': 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz',
                'filename': os.path.join(path, 'GeoLite2-City.mmdb.gz'),
                'extract_name': os.path.join(path, 'GeoLite2-City.mmdb'),
            }
        ]

        # Create GeoIP directory if it doesn't exist.
        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except FileNotFoundError:
            os.makedirs(path)

        # Download geolite binaries
        for item in files:
            self.download_and_extract_file(item)
            os.remove(item.get('filename'))
