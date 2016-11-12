import collections
import datetime
import json
from os.path import join

from django.conf import settings


def dump_request(request):
    request_data = serialize_request(request.META)

    filename = 'request-{}.json'.format(
        datetime.datetime.now().strftime('%s')
    )
    path = join(settings.ROOT_DIR, settings.REQUEST_LOG_DIR, filename)

    with open(path, 'wt') as data_file:
        data_file.write(
            json.dumps(request_data, indent=2)
        )


def serialize_request(data):
    request_data = collections.OrderedDict()
    for key in sorted(data.keys()):
        value = data[key]
        if not isinstance(value, (str, int, float, list, dict)):
            request_data[key] = str(value)
        else:
            request_data[key] = value
    return request_data
