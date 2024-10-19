import pika
import json
import datetime

# Diccionario para almacenar los reportes generados
report_storage = {}

# Función para generar 10 reportes
def generate_reports():
    for i in range(1, 11):
        report = {
            'user_id': i,
            'date': str(datetime.date(2024, 10, i)),  # Fechas de ejemplo
            'transactions': [
                {'item': f'Product {i*2-1}', 'amount': 100 + i},
                {'item': f'Product {i*2}', 'amount': 200 + i}
            ]
        }
        report_storage[i] = report
        print(f"Reporte creado para el usuario {i}: {report}")

# Función para enviar reportes en respuesta a una solicitud de lectura
def send_report_to_user_device(user_id, channel):
    report = report_storage.get(user_id)
    if report:
        # Publicar el reporte en la cola de userDevice
        channel.basic_publish(
            exchange='bus_mensajeria',  # El exchange configurado en RabbitMQ
            routing_key='userDevice.read_response',  # Cola para respuestas de lectura
            body=json.dumps(report)
        )
        print(f"Reporte enviado para el usuario {user_id}: {report}")
    else:
        print(f"Reporte no encontrado para el usuario {user_id}")

# Función para procesar solicitudes de lectura de reportes
def callback_report(ch, method, properties, body):
    message = json.loads(body)
    user_id = message.get('user_id')
    print(f"Solicitud recibida para leer el reporte del usuario {user_id}")
    send_report_to_user_device(user_id, ch)

# Función para iniciar el manejador de reportes
def start_report_handler():
    """Iniciar el manejador de reportes que escucha la cola 'report_queue'"""
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Declarar la cola (por si no ha sido creada) y enlazarla al exchange
    channel.queue_declare(queue='report_queue', arguments={'x-max-priority': 10})
    
    # Enlazar la cola al exchange 'bus_mensajeria'
    channel.queue_bind(exchange='bus_mensajeria', queue='report_queue', routing_key='report.read')

    # Consumir mensajes desde la cola report_queue
    channel.basic_consume(queue='report_queue', on_message_callback=callback_report, auto_ack=True)

    print("ReportHandler escuchando en 'report_queue'...")
    channel.start_consuming()