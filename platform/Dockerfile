FROM python:2.7
MAINTANER Zeling Feng

WORKDIR /usr/src/app

COPY requirements.txt .

COPY spawn.py .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /var/run/docker.sock

CMD [ "pypy", "spawn.py" ]
