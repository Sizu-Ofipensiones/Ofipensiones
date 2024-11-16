import pika
import json
import psycopg2

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'dbname': 'db_users',
    'user': 'postgres',
    'password': '12345',
    'host': '10.128.0.5',
    'port': '5432'
}

# Configuración de RabbitMQ
RABBITMQ_HOST = '10.128.0.4'
RABBITMQ_USER = 'monitoring_user'
RABBITMQ_PASSWORD = 'isis2503'
EXCHANGE = 'bus_mensajeria'

def connect_db():
    """Conectar a la base de datos PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def procesar_mensaje(ch, method, properties, body):
    mensaje = json.loads(body)
    conexion = connect_db()
    cursor = conexion.cursor()
    
    if mensaje["action"] == "modificar_pension":
        nuevo_valor = mensaje["nuevo_valor"]
        cursor.execute("UPDATE configuracion SET pension = %s", (nuevo_valor,))
        conexion.commit()
        print(f"Valor de la pensión modificado a {nuevo_valor}")

    elif mensaje["action"] == "consultar_transacciones":
        cursor.execute("SELECT * FROM transacciones")
        transacciones = cursor.fetchall()
        print("Transacciones:", transacciones)

    elif mensaje["action"] == "pagar_factura":
        factura_id = mensaje["factura_id"]
        cursor.execute("UPDATE transacciones SET estado = 'pagado' WHERE id = %s", (factura_id,))
        conexion.commit()
        print(f"Factura {factura_id} pagada.")

    cursor.close()
    conexion.close()

def main():
    """Configurar y ejecutar el microservicio que escucha solicitudes en RabbitMQ."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')
    channel.queue_declare(queue='userDevice.read_response')
    channel.queue_bind(exchange=EXCHANGE, queue='userDevice.read_response', routing_key='userDevice.read_response')

    print("Microservicio escuchando en la cola 'userDevice.read_response'...")
    channel.basic_consume(queue='userDevice.read_response', on_message_callback=procesar_mensaje, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
