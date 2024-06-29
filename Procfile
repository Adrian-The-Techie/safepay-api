release: python manage.py makemigrations && python manage.py migrate
web: daphne api.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
celery: celery -A api worker -l info
