FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y install python3.8
RUN apt-get -y install python3-pip
WORKDIR /code
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8081
RUN cd /code
CMD [ "python3", "manage.py" ]