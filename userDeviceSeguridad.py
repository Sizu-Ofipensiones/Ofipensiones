import pika
import json

# Configuración de RabbitMQ
RABBITMQ_HOST = '10.128.0.4'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'monitoring_user'
RABBITMQ_PASSWORD = 'isis2503'
EXCHANGE = 'bus_mensajeria'

# Definir los usuarios directamente en el archivo Python
usuarios = [
    {"email": "admin@example.com", "password": "admin123", "role": "administrador"},
    {"email": "acudiente@example.com", "password": "acudiente123", "role": "acudiente"},
    {"email": "estudiante@example.com", "password": "estudiante123", "role": "estudiante"}
]

# Conectar con RabbitMQ
def connect_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/', credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')
    return connection, channel

# Función para autenticar al usuario
def autenticar_usuario(email, password):
    for usuario in usuarios:
        if usuario["email"] == email and usuario["password"] == password:
            return usuario
    return None

# Función para enviar solicitudes a RabbitMQ
def enviar_a_rabbitmq(mensaje, routing_key):
    connection, channel = connect_rabbitmq()
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(mensaje)
    )
    print(f"Mensaje enviado a RabbitMQ: {mensaje}")
    connection.close()

# Función para escuchar respuestas desde RabbitMQ
def listen_for_responses():
    connection, channel = connect_rabbitmq()
    channel.queue_declare(queue='userDevice.read_response')
    channel.queue_bind(exchange=EXCHANGE, queue='userDevice.read_response', routing_key='userDevice.read_response')

    def callback(ch, method, properties, body):
        response = json.loads(body)
        if "error" in response:
            print(f"Error recibido: {response['error']}")
        elif "user_id" in response:
            print(f"Reporte recibido para el usuario {response['user_id']}: {response}")
        else:
            print("Mensaje desconocido recibido:", response)

    channel.basic_consume(queue='userDevice.read_response', on_message_callback=callback, auto_ack=True)
    print("Esperando respuestas de los microservicios...")
    channel.start_consuming()

# Menú según el rol del usuario
def mostrar_menu(role, email):
    while True:
        print("\n--- Menú de Usuario ---")
        if role == "administrador":
            print("1. Modificar valor de la pensión")
            print("2. Consultar todas las transacciones")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                nuevo_valor = input("Ingrese el nuevo valor de la pensión: ")
                mensaje = {"action": "modificar_pension", "email": email, "nuevo_valor": nuevo_valor}
                enviar_a_rabbitmq(mensaje, "admin.modify_pension")
            elif opcion == "2":
                mensaje = {"action": "consultar_transacciones", "email": email}
                enviar_a_rabbitmq(mensaje, "admin.read_transactions")
            elif opcion == "3":
                break
        elif role == "acudiente":
            print("1. Pagar una factura de pensión")
            print("2. Consultar mis transacciones")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                factura_id = input("Ingrese el ID de la factura: ")
                mensaje = {"action": "pagar_factura", "email": email, "factura_id": factura_id}
                enviar_a_rabbitmq(mensaje, "acudiente.pay_invoice")
            elif opcion == "2":
                mensaje = {"action": "consultar_transacciones", "email": email}
                enviar_a_rabbitmq(mensaje, "acudiente.read_transactions")
            elif opcion == "3":
                break
        elif role == "estudiante":
            print("1. Consultar transacciones de mi acudiente")
            print("2. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                mensaje = {"action": "consultar_transacciones_acudiente", "email": email}
                enviar_a_rabbitmq(mensaje, "estudiante.read_acudiente_transactions")
            elif opcion == "2":
                break

def main():
    print("=== Inicio de Sesión ===")
    email = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")
    
    usuario = autenticar_usuario(email, password)
    
    if usuario:
        print(f"\nInicio de sesión exitoso. Bienvenido {usuario['role'].capitalize()}!")
        mostrar_menu(usuario["role"], email)
        # Después de mostrar el menú, empezar a escuchar las respuestas
        listen_for_responses()
    else:
        print("\nError: Email o contraseña incorrectos.")

if __name__ == "__main__":
    main()
