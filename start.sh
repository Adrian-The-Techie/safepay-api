# bash
# start.sh

# Start the Celery worker
celery -A api worker --loglevel=info


python manage.py runserver

