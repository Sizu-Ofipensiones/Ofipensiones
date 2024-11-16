import pika
import json
import uuid

class RPCClient:
    def __init__(self, queue='user.login'):
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                '10.128.0.4',
                5672,
                '/',
                pika.PlainCredentials('monitoring_user', 'isis2503')
            )
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='bus_mensajeria',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                content_type='application/json'
            ),
            body=json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def close(self):
        self.connection.close()

def send_message_to_queue(queue, message, jwt_token=None):
    # Conectar con RabbitMQ
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials)
    )
    channel = connection.channel()

    # Incluir el token JWT en las propiedades del mensaje
    properties = pika.BasicProperties(
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt_token}'} if jwt_token else {}
    )

    # Publicar el mensaje en el exchange ya existente
    channel.basic_publish(
        exchange='bus_mensajeria',
        routing_key=queue,
        body=json.dumps(message),
        properties=properties
    )
    
    print(f"Mensaje enviado a {queue}: {message}")
    connection.close()

def request_report_detail(report_id, jwt_token):
    message = {'action': 'read', 'report_id': report_id}
    send_message_to_queue('report.read', message, jwt_token)

def main():
    # Paso 1: Solicitar inicio de sesión
    email = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")

    rpc = RPCClient(queue='user.login')
    login_message = {'email': email, 'password': password}
    print("Enviando solicitud de inicio de sesión...")
    response = rpc.call(login_message)
    rpc.close()

    if response.get('success'):
        jwt_token = response.get('token')
        user_role = response.get('role')
        print(f"Inicio de sesión exitoso. Rol: {user_role}")
    else:
        print("Error de autenticación:", response.get('message'))
        return

    # Paso 2: Crear solo 3 usuarios con roles específicos
    usuarios = [
        {
            'action': 'create',
            'name': 'Administrador',
            'email': 'admin@example.com',
            'password': 'adminpass123',
            'role': 'administrador'
        },
        {
            'action': 'create',
            'name': 'Padre',
            'email': 'padre@example.com',
            'password': 'padrepass123',
            'role': 'padre'
        },
        {
            'action': 'create',
            'name': 'Estudiante',
            'email': 'estudiante@example.com',
            'password': 'estudiantepass123',
            'role': 'estudiante'
        }
    ]
    
    print("\nCreando usuarios específicos...\n")
    for usuario in usuarios:
        send_message_to_queue('user.create', usuario, jwt_token)
        # Log de creación del usuario
        print(f"Usuario creado: Email: {usuario['email']}, Contraseña: {usuario['password']}\n")
    
    # Opcional: Puedes eliminar las siguientes secciones si no necesitas enviar solicitudes de pago o reportes
    # Paso 3: Enviar solicitudes de pago (si es necesario)
    pagos = [
        {'action': 'process', 'amount': 100, 'currency': 'USD', 'user_id': 1},
        {'action': 'process', 'amount': 250, 'currency': 'USD', 'user_id': 2},
        {'action': 'process', 'amount': 500, 'currency': 'EUR', 'user_id': 1},
    ]
    
    for pago in pagos:
        send_message_to_queue('payment.process', pago, jwt_token)
    
    # Paso 4: Solicitar la lectura del reporte con ID 1
    request_report_detail(1, jwt_token)

if __name__ == "__main__":
    main()
