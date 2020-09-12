service cron start
crontab /code/cronjob
bash -c "/usr/local/bin/python3.6 manage.py runserver 0.0.0.0:8081"