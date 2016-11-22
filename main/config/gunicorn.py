import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

raw_env = 'DJANGO_SETTINGS_MODULE=config.production'

HOST = '0.0.0.0'

PORT = '8000'

bind = '{}:{}'.format(HOST, PORT)

accesslog = '/app/log/gunicorn-access.log'

errorlog = '/app/log/gunicorn-error.log'

workers = 1

reload = True
