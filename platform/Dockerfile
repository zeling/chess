FROM pypy:2-5.9.0

WORKDIR /usr/src/app

COPY requirements.txt .

COPY spawn.py .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /var/run/docker.sock /var/run/docker.sock

CMD [ "pypy", "spawn.py" ]
