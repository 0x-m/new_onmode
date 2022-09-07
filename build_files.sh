pip install -r ./requirements/prod.txt
python3 manage.py collectstatic
python manage.py migrate
