import pika
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Función para enviar una solicitud de lectura de reporte
def send_read_request(user_id):
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Crear el mensaje de solicitud de lectura del reporte para el usuario
    message = {'user_id': user_id}

    # Publicar el mensaje en el exchange de RabbitMQ
    channel.basic_publish(
        exchange='bus_mensajeria',  # El exchange configurado en RabbitMQ
        routing_key='report.read',  # Cola de solicitudes de lectura
        body=json.dumps(message)
    )

    connection.close()

# Función para medir el tiempo de respuesta
def measure_response_time(user_id):
    start_time = time.time()  # Marcar el inicio del envío
    send_read_request(user_id)
    end_time = time.time()  # Marcar el final después del envío
    return end_time - start_time

# Prueba de carga para 3000 solicitudes concurrentes
def load_test_concurrent():
    num_requests = 3000  # 3000 usuarios
    user_ids = range(1, num_requests + 1)  # Simular 3000 usuarios con IDs únicos
    total_time = 0

    # Usar ThreadPoolExecutor para manejar 3000 hilos (usuarios) concurrentes
    with ThreadPoolExecutor(max_workers=3000) as executor:
        futures = [executor.submit(measure_response_time, user_id) for user_id in user_ids]

        # Esperar a que todas las solicitudes se completen y recolectar tiempos
        response_times = []
        for future in as_completed(futures):
            response_times.append(future.result())

    # Calcular el tiempo promedio de respuesta
    avg_time = sum(response_times) / num_requests
    print(f"El tiempo promedio de respuesta para 3000 usuarios concurrentes fue de {avg_time} segundos.")

if __name__ == "__main__":
    load_test_concurrent()