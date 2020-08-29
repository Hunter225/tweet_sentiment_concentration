FROM python:3.6
RUN apt-get update && apt-get -y install cron vim rsyslog
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8081
ENTRYPOINT bash -c "chmod 700 /code/start.sh;/code/start.sh"
