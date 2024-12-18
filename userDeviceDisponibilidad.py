import pika
import json

# Función para enviar solicitudes de lectura de reporte al manejador de reportes
def send_read_request(user_id):
    # Conectar con RabbitMQ (con la IP de la VM donde está RabbitMQ)
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Crear el mensaje de solicitud de lectura del reporte para el usuario
    message = {'user_id': user_id}

    # Publicar el mensaje en el exchange de RabbitMQ (cola de solicitudes)
    channel.basic_publish(
        exchange='bus_mensajeria',  # El exchange configurado en RabbitMQ
        routing_key='report.read',  # Cola de solicitudes de lectura
        body=json.dumps(message)
    )

    print(f"Solicitud de lectura enviada para el usuario {user_id}")
    connection.close()

# Función para escuchar las respuestas de lectura de reportes
def listen_for_report_responses():
    # Conectar con RabbitMQ (misma instancia de RabbitMQ, accesible desde esta VM)
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Declarar el exchange 'bus_mensajeria' si no ha sido creado
    channel.exchange_declare(exchange='bus_mensajeria', exchange_type='topic')

    # Declarar la cola donde escucharemos las respuestas de los reportes (userDevice.read_response)
    channel.queue_declare(queue='userDevice.read_response')

    # Enlazar la cola al exchange para recibir los mensajes de respuesta
    channel.queue_bind(exchange='bus_mensajeria', queue='userDevice.read_response', routing_key='userDevice.read_response')

    # Callback para manejar la respuesta del reporte
    def callback(ch, method, properties, body):
        response = json.loads(body)
        
        # Verificar si el mensaje contiene un campo de error
        if "error" in response:
            print(f"Error recibido: {response['error']}")
        elif "user_id" in response:
            # Procesar el reporte si no es un mensaje de error
            print(f"Reporte recibido para el usuario {response['user_id']}: {response}")
        else:
            print("Mensaje desconocido recibido:", response)

    # Consumir los mensajes de la cola de respuestas
    channel.basic_consume(queue='userDevice.read_response', on_message_callback=callback, auto_ack=True)

    print("Esperando respuestas de reportes...")
    channel.start_consuming()

# Ejecutar el script
if __name__ == "__main__":
    # Enviar una solicitud para el reporte del usuario 1
    send_read_request(1)

    # Escuchar las respuestas de los reportes
    listen_for_report_responses()
