python manage.py migrate --no-input
gunicorn api_yamdb.wsgi:application --bind 0:8000
