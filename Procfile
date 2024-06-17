release: python manage.py makemigrations && python manage.py migrate && python -m celery -A api worker -l info
web: gunicorn api.wsgi --log-file -