python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
#/usr/local/bin/gunicorn server.wsgi \
#  --workers=4 \
#  --max-requests=2000 \
#  --timeout=60 \
#  --max-requests-jitter=400 \
#  --bind='0.0.0.0:8000' \
#  --chdir='/code' \
#  --log-file=- \
#  --worker-tmp-dir='/dev/shm'