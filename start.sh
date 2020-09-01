bash -c "service cron start"
bash -c "/usr/local/bin/python3.6 manage.py crontab add"
bash -c "/usr/local/bin/python3.6 manage.py runserver 0.0.0.0:8081"