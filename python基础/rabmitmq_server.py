#coding=utf-8
import pika
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def rab_server():
    connection =pika.BlockingConnection(pika.ConnectionParameters("localhost",5672))
    channel=connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',routing_key='hello',body='师姐你好')
    print "[x] send 'hello world'"
    connection.close()

if __name__ == '__main__':
    rab_server()