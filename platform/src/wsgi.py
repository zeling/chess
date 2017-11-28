from gevent import monkey; monkey.patch_all()
from bottle import Bottle, request, run
from pg_plugin import PGPlugin
import tasks

app = application = Bottle()
app.install(PGPlugin(host='localhost', dbname='postgres', user='postgres', password='M4rkf3ng', maxsize=3))

@app.get('/')
def root(pool):
    pool.execute('SELECT pg_sleep(3);')
    return '42'

@app.post('/user')
def create_user(pool):
    pass

@app.post('/token')
def token(pool):
    auth_data = request.json
    pool.fetchone('SELECT * FROM users WHERE user_id = ?', auth_data.name)
    return "42"

  

run(app, host='0.0.0.0', port=8080, server='gevent')
