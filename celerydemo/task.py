#coding=utf-8
from celery import Celery
from celery.bin import worker as celery_worker
import celeryconfig
import sys

broker = 'amqp://'
backend = 'amqp'
app = Celery('task', backend=backend, broker=broker)

@app.task
def mytask0(task_name):
    print ("task0:%s" %task_name)
    print(sys.path)
    return task_name

@app.task
def mytask1(task_name):
    print ("task1:%s" %task_name)
    return task_name

def worker_start():
    worker = celery_worker.worker(app=app)
    worker.run(broker=broker, concurrency=4,
               traceback=False, loglevel='INFO')

if __name__ == "__main__":
    print(sys.path)
    sys.path.append("C:\\Users\\lgc\\Desktop\\code")
    worker_start()

