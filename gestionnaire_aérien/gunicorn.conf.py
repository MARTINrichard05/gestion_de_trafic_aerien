command = '/usr/bin/gunicorn'
pythonpath = '.'
bind = 'unix:/home/kali/gestionnaire_aérien/gestionnaire_aérien.sock'
workers = 3
user = 'kali'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=gestionnaire_aérien.settings'