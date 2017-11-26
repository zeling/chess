from bottle import Bottle, request, run
from agent import respond_to

app = application = Bottle()

@app.post('/api/movement')
def make_decision():
  return respond_to(request.body.read())

run(app, host='0.0.0.0', port=8080)

