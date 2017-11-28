FROM python:2.7
MAINTAINER Zeling Feng

WORKDIR /usr/src/app

COPY requirements.txt .

COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /var/run/docker.sock

CMD [ "python", "wsgi.py" ]
