import pika
import json

# Función para enviar solicitudes de lectura de reporte al manejador de reportes
def send_read_request(user_id):
    # Conectar con RabbitMQ
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Crear el mensaje de solicitud de lectura del reporte para el usuario
    message = {'user_id': user_id}

    # Publicar el mensaje en el exchange de RabbitMQ
    channel.basic_publish(
        exchange='bus_mensajeria',  # El exchange configurado en RabbitMQ
        routing_key='report.read',  # Enrutamiento para solicitudes de lectura de reportes
        body=json.dumps(message)
    )

    print(f"Solicitud de lectura enviada para el usuario {user_id}")
    connection.close()

# Escuchar las respuestas de lectura de reportes
def listen_for_report_responses():
    # Conectar con RabbitMQ
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Declarar la cola donde escucharemos las respuestas de los reportes
    channel.queue_declare(queue='userDevice.read_response')

    # Callback para manejar la respuesta del reporte
    def callback(ch, method, properties, body):
        report = json.loads(body)
        print(f"Reporte recibido para el usuario {report['user_id']}: {report}")

    # Consumir los mensajes de la cola
    channel.basic_consume(queue='userDevice.read_response', on_message_callback=callback, auto_ack=True)

    print("Esperando respuestas de reportes...")
    channel.start_consuming()

# Ejecutar el script
if _name_ == "_main_":
    # Enviar una solicitud para el reporte del usuario 1
    send_read_request(1)

    # Escuchar las respuestas de los reportes
    listen_for_report_responses()