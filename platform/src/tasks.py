from celery import Celery
from time import sleep
from base64 import b64decode
from tempfile import mkstemp, mkdtemp
from docker import DockerClient
from shutil import rmtree
import os
import errno
import tarfile
import smtplib
import requests

REPO = 'registry:5000'

app = Celery('tasks', broker='amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq'.format(**os.environ), backend="amqp")

def get_docker():
    return DockerClient('unix:///var/run/docker.sock', version='1.24')

def img_tag(stu_id):
    return '{}/chess/{}:latest'.format(REPO, stu_id)

@app.task
def fetch_movement(stu_id, fen):
    return requests.post('http://{stu_id}:8080/api/movement'.format(**locals()), fen).text

@app.task
def deploy(stu_id, submission):
    try:
        content = b64decode(submission)
        tmpdir = mkdtemp(prefix=stu_id)
        (t, tarname) = mkstemp(prefix=stu_id, suffix='.tgz', dir=tmpdir)
        os.write(t, content)
        os.close(t)
        with tarfile.open(name=tarname, mode='r|gz') as tar:
            tar.extractall(path=tmpdir)
        kill(stu_id)
        docker = get_docker()
        img = docker.images.build(path=tmpdir, tag=img_tag(stu_id))
        docker.images.push(img_tag(stu_id))
        return img.id
    except:
        raise
    finally:
        try:
            rmtree(tmpdir)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
@app.task
def launch(stu_id):
    docker = get_docker()
    if docker.containers.list(filters={'name': stu_id}):
       raise RuntimeError('You have already launched your instance')
    else:
       ctn = docker.containers.run(img_tag(stu_id), cpu_period=100000, cpu_quota=100000, detach=True, name=stu_id, mem_limit='64m', network='platform_default')
       return ctn.id

@app.task
def kill(stu_id):
    docker = get_docker()
    cs = docker.containers.list(filters={'name': stu_id})
    if cs:
	c = cs[0]
        id = c.id
        c.kill()
        c.remove()
        return id
    else:
        raise RuntimeError('You have not lauched your instance')

@app.task
def list_agents():
    return requests.get('http://{REPO}/v2/_catalog'.format(**globals())).json()

@app.task
def sendmail(stu_id, subject, content):
    smtp = smtplib.SMTP()
    smtp.connect('smtp.live.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('zeling.feng@hotmail.com', os.environ('MAIL_PASS'))
    
