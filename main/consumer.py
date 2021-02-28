from main import Product, db
import pika
import json


params = pika.URLParameters(
    'amqps://nahnbicl:nti9nhuNg1bCq6QHXoEgNn51hw7lwGyL@shrimp.rmq.cloudamqp.com/nahnbicl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(body)

    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commite()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Created')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
