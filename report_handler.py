import pika
import json
import datetime
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

# Diccionario para almacenar los reportes generados
report_storage = {}

# Lista de URLs de health check de cada instancia del microservicio de reportes
report_instances = [
    "http://10.128.0.7:8080/health-check/",
    "http://10.128.0.8:8080/health-check/",
    "http://10.128.0.9:8080/health-check/",
    "http://10.128.0.10:8080/health-check/"
]

# Función para generar 10 reportes quemados
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

# Función para verificar el estado de las instancias de reportes
def check_instance_health():
    healthy_instances = 0
    for url in report_instances:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                healthy_instances += 1
        except requests.RequestException:
            continue
    return healthy_instances

# Función para enviar reportes en respuesta a una solicitud de lectura
def send_report_to_user_device(user_id, channel):
    # Verificar el número de instancias saludables
    healthy_instances = check_instance_health()
    total_instances = len(report_instances)

    # Si menos del 25% de las instancias están saludables, enviar mensaje de error
    if healthy_instances <= total_instances * 0.25:
        error_message = {
            'error': "El servicio de reportes no está disponible en este momento. Por favor, intente más tarde."
        }
        channel.basic_publish(
            exchange='bus_mensajeria',
            routing_key='userDevice.read_response',
            body=json.dumps(error_message)
        )
        print("Error enviado: menos del 25% de las instancias de reportes están operativas.")
        return

    # Obtener y enviar el reporte si el servicio está operativo
    report = report_storage.get(user_id)
    if report:
        try:
            print(f"Enviando reporte para el usuario {user_id} a la cola 'userDevice.read_response'...")
            channel.basic_publish(
                exchange='bus_mensajeria',  # El exchange configurado en RabbitMQ
                routing_key='userDevice.read_response',  # Cola para respuestas de lectura
                body=json.dumps(report)
            )
            print(f"Reporte enviado para el usuario {user_id}: {report}")
        except Exception as e:
            print(f"Error enviando el reporte para el usuario {user_id}: {e}")
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
    """Iniciar el manejador de reportes que escucha la cola 'report_queue' para solicitudes de lectura"""
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Declarar el exchange 'bus_mensajeria' si no ha sido creado
    channel.exchange_declare(exchange='bus_mensajeria', exchange_type='topic')

    # Declarar la cola (por si no ha sido creada) y enlazarla al exchange
    channel.queue_declare(queue='report_queue', arguments={'x-max-priority': 10})
    
    # Enlazar la cola al exchange 'bus_mensajeria' usando el routing_key 'report.read'
    channel.queue_bind(exchange='bus_mensajeria', queue='report_queue', routing_key='report.read')

    # Consumir mensajes desde la cola de solicitudes
    channel.basic_consume(queue='report_queue', on_message_callback=callback_report, auto_ack=True)

    print("ReportHandler escuchando en 'report_queue'...")
    channel.start_consuming()

# Servidor HTTP básico para responder a los health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health-check/':
            # Responder con un status 200 OK para los health checks
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    server_address = ('', 8080)  # Escuchar en el puerto 8080
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print("Servidor HTTP para health checks escuchando en el puerto 8080...")
    httpd.serve_forever()

# Iniciar tanto el servidor HTTP como el report handler
if __name__ == "__main__":
    # Crear los 10 reportes inicialmente
    generate_reports()

    # Iniciar el manejador de reportes en un hilo separado
    report_thread = threading.Thread(target=start_report_handler)
    report_thread.daemon = True
    report_thread.start()

    # Iniciar el servidor HTTP para los health checks
    start_http_server()
