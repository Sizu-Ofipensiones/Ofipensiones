import pika
import json

def callback_report(ch, method, properties, body):
    """Callback que procesa las solicitudes relacionadas con reportes"""
    payload = json.loads(body.decode('utf8'))# Decodificar el mensaje
    action = payload.get('action') # Obtener la acción a realizar

    if action == 'process':
        process_report(payload)

    print(f"Procesando {action} para el reporte de usuario: {payload.get('user_id')}")

def process_report(data):
    """Procesar un reporte (simulado)"""
    print(f"Procesando reporte de {data['amount']} {data['currency']} para el usuario {data['user_id']}")

def start_report_handler():
    """Iniciar el manejador de reportes que escucha la cola 'report_queue'"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar la cola (por si no ha sido creada) y enlazarla al exchange
    channel.queue_declare(queue='report_queue', arguments={'x-max-priority': 10})
    
    # Enlazar la cola al exchange 'bus_mensajeria'
    channel.queue_bind(exchange='bus_mensajeria', queue='report_queue', routing_key='report.#')

    # Consumir mensajes desde la cola report_queue
    channel.basic_consume(queue='report_queue', on_message_callback=callback_report, auto_ack=True)

    print("PaymentHandler escuchando en 'report_queue'...")
    channel.start_consuming()

if __name__ == "__main__":
    start_report_handler()