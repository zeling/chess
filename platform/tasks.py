from celery import Celery
from time import sleep

app = Celery('tasks', broker='amqp://guest:guest@localhost', backend="amqp")

@app.task
def add(x, y):
    sleep(3)
    return x + y

