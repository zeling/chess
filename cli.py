import requests
import click
import getpass
import sys
from tempfile import mkstemp
import tarfile
import os
from base64 import b64encode
import json

SERVER_URI = 'http://10.141.209.144:54321'
HEADERS = { 'Content-Type': 'application/json' }

def ask_cred():
    sys.stdout.write('Student Id: ')
    return (raw_input(), getpass.getpass())

@click.group()
def cli():
    pass

@cli.command()
def register():
    sys.stdout.write('Student Id: ')
    stu_id = raw_input()

@cli.command()
def login():
    (u, p) = ask_cred()
    print "{SERVER_URI}/token".format(**globals())

@cli.command()
def list():
    for r in requests.get('{SERVER_URI}/agents'.format(**globals())).json()[u'repositories']:
        click.echo(r)

@cli.command()
@click.argument('stu_id')
@click.argument('path', default=os.path.join(os.getcwd(), 'agent'))
def deploy(stu_id, path):
    path = os.path.normpath(path)
    (fd, name) = mkstemp()
    if os.path.isfile(os.path.join(path, 'Dockerfile')):
        with os.fdopen(fd, 'r+') as f:
            with tarfile.open(fileobj=f, mode='w|gz') as tgz:
                old_dir = os.getcwd()
                os.chdir(path)
                tgz.add('.')
                os.chdir(old_dir)
            f.seek(0)
            content = b64encode(f.read())
        os.remove(name)
        r = requests.post('{SERVER_URI}/deploy'.format(**globals()), data=json.dumps({'stu_id': stu_id, 'content': content}), headers=HEADERS)
        if r.status_code == requests.codes.ok:
            click.echo(r.text)
        else:
            click.echo(r.json()[u'reason'])
    else:
        click.echo('you should specify a directory with a Dockerfile')

@cli.command()
@click.argument('stu_id')
def launch(stu_id):
    r = requests.post('{SERVER_URI}/launch'.format(**globals()), data=json.dumps({'stu_id': stu_id}), headers=HEADERS)
    if r.status_code == requests.codes.ok:
        click.echo(r.text)
    else:
        click.echo(r.json()[u'reason'])

@cli.command()
@click.argument('stu_id')
def kill(stu_id):
    r = requests.post('{SERVER_URI}/kill'.format(**globals()), data=json.dumps({'stu_id': stu_id}), headers=HEADERS)
    if r.status_code == requests.codes.ok:
        click.echo(r.text)
    else:
        click.echo(r.json()[u'reason'])

if __name__ == '__main__':
    cli()
