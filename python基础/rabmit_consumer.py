#coding=utf-8
import pika
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def rab_consume():
    connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel=connection.channel()
    channel.queue_declare(queue='hello')

    def callback(ch,method,properties,body):
        print ch,method,properties
        print(" [x] Received %r" % body)
        time.sleep(15)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(callback,queue='hello')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  # 开始消费消息

if __name__ == '__main__':
    rab_consume()