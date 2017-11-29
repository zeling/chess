import requests
import click
import getpass
import sys
from tempfile import mkstemp
import tarfile
import os
from base64 import b64encode

SERVER_URI = 'http://10.141.209.144:4321'

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
@click.argument('path', default=os.path.join(os.getcwd(), 'agent'))
def deploy(path):
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
    else:
        click.echo('you should specify a directory with a Dockerfile')

@cli.command()
def start():
    pass

@cli.command()
def stop():
    pass

if __name__ == '__main__':
    cli()
