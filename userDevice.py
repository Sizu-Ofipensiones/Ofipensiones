import pika
import json

def send_message_to_queue(queue, message):
    # Conectar con RabbitMQ
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Publicar el mensaje en el exchange ya existente (declarado por el bus de mensajería)
    channel.basic_publish(
        exchange='bus_mensajeria',  # Usar el exchange ya configurado por el bus
        routing_key=queue,  # Puede ser 'user.create', 'payment.process', etc.
        body=json.dumps(message)
    )
    
    print(f"Mensaje enviado a {queue}: {message}")
    connection.close()

# Enviar múltiples solicitudes de CRUD de usuarios
usuarios = [
    {'action': 'create', 'name': 'Juan', 'email': 'juan@example.com', 'password': 'password123', 'position': 'Gerente'},
    {'action': 'create', 'name': 'Ana', 'email': 'ana@example.com', 'password': 'password123', 'position': 'Desarrolladora'},
    {'action': 'update', 'id': 1, 'name': 'Juan Actualizado', 'email': 'juan.updated@example.com', 'position': 'Director'},
    {'action': 'delete', 'id': 2},  # Borrar un usuario por ID
]

for usuario in usuarios:
    send_message_to_queue('user.' + usuario['action'], usuario)

# Enviar múltiples solicitudes de pago
pagos = [
    {'action': 'process', 'amount': 100, 'currency': 'USD', 'user_id': 1},
    {'action': 'process', 'amount': 250, 'currency': 'USD', 'user_id': 2},
    {'action': 'process', 'amount': 500, 'currency': 'EUR', 'user_id': 1},
]

for pago in pagos:
    send_message_to_queue('payment.process', pago)

# Función para solicitar la lectura de un reporte por ID
def request_report_detail(report_id):
    message = {'action': 'read', 'report_id': report_id}
    send_message_to_queue('report.read', message)
# Ejecutar el script
if _name_ == "_main_":
    # Solicitar la lectura del reporte con ID 1
    request_report_detail(1)