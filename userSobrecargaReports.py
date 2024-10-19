import pika
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lista de los 10 userId disponibles
user_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
    try:
        send_read_request(user_id)
        end_time = time.time()  # Marcar el final después del envío
        return end_time - start_time, False  # False indica que no hubo error
    except Exception as e:
        print(f"Error al enviar la solicitud para el usuario {user_id}: {e}")
        return 0, True  # True indica que hubo un error

# Prueba de carga para solicitudes concurrentes utilizando 10 userId
def load_test_concurrent():
    num_requests = int(input("Ingrese la cantidad de peticiones:"))
    total_time = 0
    error_count = 0

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(measure_response_time, user_ids[i % 10]) for i in range(num_requests)]

        # Esperar a que todas las solicitudes se completen y recolectar tiempos
        response_times = []
        for future in as_completed(futures):
            response_time, error_occurred = future.result()
            if not error_occurred:
                response_times.append(response_time)
            else:
                error_count += 1

    # Calcular el tiempo promedio de respuesta solo para las solicitudes exitosas
    if response_times:
        avg_time = sum(response_times) / len(response_times)
    else:
        avg_time = 0

    # Calcular el porcentaje de errores
    error_percentage = (error_count / num_requests) * 100

    print(f"El tiempo promedio de respuesta para {num_requests} usuarios concurrentes fue de {avg_time} segundos.")
    print(f"El porcentaje de errores fue del {error_percentage:.2f}%.")

if __name__ == "__main__":
    load_test_concurrent()