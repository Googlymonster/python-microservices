import pika
import json

params = pika.URLParameters(
    'amqps://nahnbicl:nti9nhuNg1bCq6QHXoEgNn51hw7lwGyL@shrimp.rmq.cloudamqp.com/nahnbicl')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main',
                          body=json.dumps(body), properties=properties)
