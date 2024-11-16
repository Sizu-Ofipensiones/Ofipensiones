import pika
import json
import requests
import logging

# Configuración de los logs
logging.basicConfig(
    level=logging.DEBUG,  # Cambia a INFO o ERROR en producción
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuración de Auth0
AUTH0_DOMAIN = 'dev-xitt1wu7afthncmv.us.auth0.com'
CLIENT_ID = 'TTmqAS6niW6L9heQPuNX650m7wLrHWpk'
CLIENT_SECRET = 'tTRaEYXFEgtKYW3xCGVVxCCTgcJp_elcfoPaISz4M7L_EkIX-Fbg-1Fg51wR7rj6'
AUDIENCE = 'https/users/api'

def authenticate_user():
    """
    Solicitar credenciales al usuario y autenticarse en Auth0.
    """
    logging.info("Iniciando el proceso de autenticación del usuario.")
    username = input("Usuario (email): ")
    password = input("Contraseña: ")

    # Construir la URL para obtener el token
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'audience': AUDIENCE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'openid profile email'
    }

    logging.debug(f"Payload enviado al endpoint /oauth/token: {payload}")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        token = data.get('access_token')

        if token:
            logging.info("Autenticación exitosa. Token obtenido.")
            return token
        else:
            logging.error("No se pudo obtener el token. Respuesta incompleta.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al autenticar: {e}")
        return None

def get_user_roles(token):
    """
    Recupera los roles del usuario autenticado desde el token JWT.
    """
    logging.info("Solicitando roles del usuario desde /userinfo.")
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {'Authorization': f'Bearer {token}'}

    logging.debug(f"Headers enviados a /userinfo: {headers}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        logging.debug(f"Datos del usuario obtenidos: {user_data}")

        roles = user_data.get("https://example.com/roles", [])
        user_id = user_data.get("sub", "unknown")

        logging.info(f"Roles obtenidos: {roles}, User ID: {user_id}")
        return roles, user_id
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener roles del usuario: {e}")
        return [], "unknown"

def send_message_to_queue(queue, message, roles, user_id):
    """
    Envía un mensaje a RabbitMQ validando los roles primero.
    """
    logging.info(f"Intentando enviar mensaje a la cola '{queue}' con roles: {roles}.")
    
    # Validar acceso según rol
    if "Administrador" in roles:
        logging.info("Acceso concedido: Administrador.")
    elif "Padre" in roles and message.get("user_id") == user_id:
        logging.info("Acceso concedido: Padre.")
    else:
        logging.warning("Acceso denegado. Roles insuficientes o ID de usuario no coincide.")
        return

    # Conectar con RabbitMQ
    try:
        credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
        channel = connection.channel()

        # Publicar el mensaje
        channel.basic_publish(
            exchange='bus_mensajeria',
            routing_key=queue,
            body=json.dumps(message)
        )

        logging.info(f"Mensaje enviado a la cola '{queue}': {message}")
        connection.close()
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")

def main():
    # Autenticar al usuario
    logging.info("Inicio del programa principal.")
    token = authenticate_user()
    if not token:
        logging.error("No se pudo autenticar al usuario. Saliendo del programa.")
        return

    # Obtener roles e ID del usuario
    roles, user_id = get_user_roles(token)
    if not roles:
        logging.error("No se obtuvieron roles para el usuario. Saliendo del programa.")
        return

    logging.info(f"Roles obtenidos: {roles}, User ID: {user_id}")

    # Ejemplo de datos de usuarios
    usuarios = [
        {"action": "create", "user_id": "auth0|12345", "name": "Juan", "email": "juan@example.com"},
        {"action": "create", "user_id": "auth0|67890", "name": "Ana", "email": "ana@example.com"}
    ]

    for usuario in usuarios:
        send_message_to_queue("user.create", usuario, roles, user_id)

if __name__ == "__main__":
    main()
