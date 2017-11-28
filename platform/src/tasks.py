from celery import Celery
from time import sleep
from base64 import b64decode
from tempfile import mkstemp, mkdtemp
from docker import DockerClient
import os
import tarfile


app = Celery('tasks', broker='amqp://guest:guest@localhost', backend="amqp")


@app.task
def deploy(stu_id, submission):
    content = b64decode(submission)
    tmpdir = mkdtemp(prefix=stu_id)
    (t, tarname) = mkstemp(prefix=stu_id, suffix='.tgz', dir=tmpdir)
    os.write(t, content)
    os.close(t)
    with tarfile.open(name=tarname, mode='r:gz') as tar:
        tar.extractall(path=tmpdir)
    img_tag = '{}/chess/{}'.format('localhost:5000', stu_id)
    docker = DockerClient('unix:///var/run/docker.sock')
    docker.images.build(path=os.path.join(tmpdir, 'agent'), tag=img_tag)
    docker.images.push(img_tag)
    

@app.task
def add(x, y):
    sleep(3)
    return x + y

