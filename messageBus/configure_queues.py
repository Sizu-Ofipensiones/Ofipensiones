import pika

def configure_queues():
    """Configura el exchange y las colas con prioridad en RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # Conectar con RabbitMQ
    channel = connection.channel()

    # Declarar el exchange tipo 'topic' centralizado
    channel.exchange_declare(exchange='bus_mensajeria', exchange_type='topic')

    # Declarar las colas con prioridad
    channel.queue_declare(queue='report_queue', arguments={'x-max-priority': 10})
    channel.queue_declare(queue='user_queue', arguments={'x-max-priority': 10})
    channel.queue_declare(queue='payment_queue', arguments={'x-max-priority': 5})

    # Enlazar las colas al exchange 'bus_mensajeria'
    channel.queue_bind(exchange='bus_mensajeria', queue='report_queue', routing_key='report.#')
    channel.queue_bind(exchange='bus_mensajeria', queue='user_queue', routing_key='user.#')
    channel.queue_bind(exchange='bus_mensajeria', queue='payment_queue', routing_key='payment.#')

    print("Colas y exchange configurados correctamente.")
    connection.close()

if __name__ == "__main__":
    configure_queues()
