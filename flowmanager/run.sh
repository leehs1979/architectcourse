python manage.py makemigrations flowmanagerapi
python manage.py migrate

python manage.py runserver 0.0.0.0:28000
#gunicorn --bind 0.0.0.0:28000 --workers 4 --threads 8 --timeout 0 flowmanager.wsgi