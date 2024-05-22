command = '/usr/bin/gunicorn'
pythonpath = '.'
bind = '127.0.0.1:8000'
workers = 3
user = 'username'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=gestionnaire_aérien.settings'