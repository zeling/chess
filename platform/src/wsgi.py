from gevent import monkey; monkey.patch_all()
from bottle import Bottle, request, run, abort
from pg_plugin import PGPlugin
from docker.errors import APIError
from celery.exceptions import TimeoutError
from contextlib import contextmanager
import tasks

app = application = Bottle()
# app.install(PGPlugin(host='localhost', dbname='postgres', user='postgres', password='', maxsize=3))

class ErrorHandler:
    def get(self, ignore, default):
        def error_handler(error):
            from json import dumps
            from bottle import tob
            return tob(dumps({ "status_code": error.status_code, "status": error.status, "reason": error.body }))
        return error_handler

app.error_handler = ErrorHandler()


@app.get('/')
def root():
    # pool.execute('SELECT pg_sleep(3);')
    return '42'

@app.post('/user')
def create_user(pool):
    pass

@app.post('/token')
def token():
    auth_data = request.json
    # pool.fetchone('SELECT * FROM users WHERE user_id = ?', auth_data.name)
    return "42"

@app.get('/agents')
def list_agents():
    with delay(tasks.list_agents) as r:
         return r.get(timeout=5)

@app.post('/api/movement')
def fetch_movement():
    stu_id = request.json['stu_id']
    fen = request.json['fen']
    with delay(tasks.fetch_movement, stu_id, fen) as r:
         return r.get(timeout=3)

@app.post('/deploy')
def deploy():
    stu_id = request.json['stu_id']
    content = request.json['content']
    with delay(tasks.deploy, stu_id, content) as r:
         r.get(timeout=10)
         return 'successfully deployed your agent'

@app.post('/launch')
def launch():
    stu_id = request.json['stu_id']
    with delay(tasks.launch, stu_id) as r:
         r.get(timeout=10)
         return 'successfully deplyed your agent'

@app.post('/kill')
def kill():
    stu_id = request.json['stu_id']
    with delay(tasks.kill, stu_id) as r:
         r.get(timeout=10)
         return 'successfully killed your agent'

@contextmanager
def delay(task, *args, **kwargs):
    try:
        yield task.delay(*args, **kwargs)
    except TimeoutError:
        abort(408, '{} has timed out'.format(task.name))
    except APIError as e:
        if e.response is not None:
            abort(e.response.status_code, str(e))
        else:
            abort(500, str(e))
    except Exception as e:
        abort(403, str(e)) 
        
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, server='gevent')

