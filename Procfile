release: python manage.py makemigrations && python manage.py migrate
web: gunicorn pigi.wsgi --log-file -