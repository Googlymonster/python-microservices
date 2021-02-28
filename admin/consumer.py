import django
from products.models import Product
import pika
import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()


params = pika.URLParameters(
    'amqps://nahnbicl:nti9nhuNg1bCq6QHXoEgNn51hw7lwGyL@shrimp.rmq.cloudamqp.com/nahnbicl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
