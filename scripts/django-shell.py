import os
from os.path import abspath, dirname, join
import sys

import django


def print_header():
    header = """
      _   _                                    _            _  _ 
   __| | (_)  __ _  _ __    __ _   ___    ___ | |__    ___ | || |
  / _` | | | / _` || '_ \  / _` | / _ \  / __|| '_ \  / _ \| || |
 | (_| | | || (_| || | | || (_| || (_) | \__ \| | | ||  __/| || |
  \__,_|_/ | \__,_||_| |_| \__, | \___/  |___/|_| |_| \___||_||_|
       |__/                |___/                                 
    """
    print(header)
    print("")


if __name__ == '__main__':
    path = join(dirname(dirname(abspath(__file__))), 'main')
    print('path: {}'.format(path))

    sys.path.insert(0, abspath(path))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    # Import Django modules.
    from django.contrib.sites.models import Site

    # Import models.
    from users.models import *
    from links.models import *

    # Easy model functions.
    uu = lambda: User.objects.all()
    ll = lambda: Link.objects.all()

    print_header()
