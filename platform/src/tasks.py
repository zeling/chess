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


app = Celery('tasks', broker='amqp://guest:guest@localhost', backend="amqp")

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
        img_tag = '{}/chess/{}'.format('localhost:5000', stu_id)
        docker = DockerClient('unix:///var/run/docker.sock')
        docker.images.build(path=tmpdir, tag=img_tag)
        docker.images.push(img_tag)

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
    docker = DockerClient('unix:///var/run/docker.sock')
    if docker.containers.list(filters={'name': stu_id}):
       raise RuntimeError('You have already launched your instance')
    else:
       img_tag = '{}/chess/{}'.format('localhost:5000', stu_id)
       container = docker.containers.run(img_tag, auto_remove=True, cpu_count=1, detach=True, name=stu_id)

@app.task
def sendmail(stu_id, subject, content):
    smtp = smtplib.SMTP()
    smtp.connect('smtp.live.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('zeling.feng@hotmail.com', os.environ('MAIL_PASS'))
    
