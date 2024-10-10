import pika
import json

def callback_payment(ch, method, properties, body):
    """Callback que procesa las solicitudes relacionadas con pagos"""
    payload = json.loads(body.decode('utf8'))# Decodificar el mensaje
    action = payload.get('action') # Obtener la acción a realizar

    if action == 'process':
        process_payment(payload)

    print(f"Procesando {action} para el pago de usuario: {payload.get('user_id')}")

def process_payment(data):
    """Procesar un pago (simulado)"""
    print(f"Procesando pago de {data['amount']} {data['currency']} para el usuario {data['user_id']}")

def start_payment_handler():
    """Iniciar el manejador de pagos que escucha la cola 'payment_queue'"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar la cola (por si no ha sido creada) y enlazarla al exchange
    channel.queue_declare(queue='payment_queue', arguments={'x-max-priority': 5})
    
    # Enlazar la cola al exchange 'bus_mensajeria'
    channel.queue_bind(exchange='bus_mensajeria', queue='payment_queue', routing_key='payment.#')

    # Consumir mensajes desde la cola payment_queue
    channel.basic_consume(queue='payment_queue', on_message_callback=callback_payment, auto_ack=True)

    print("PaymentHandler escuchando en 'payment_queue'...")
    channel.start_consuming()

if __name__ == "__main__":
    start_payment_handler()
