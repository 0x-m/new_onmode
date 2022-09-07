pip install -r ./requirements/prod.txt
python3 manage.py collectstatic
python3 manage.py migrate
