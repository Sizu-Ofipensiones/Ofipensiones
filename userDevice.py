import os
import json
import logging
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pika
import requests
from jose import jwt, JWTError, ExpiredSignatureError
from authlib.integrations.requests_client import OAuth2Session

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuración de Auth0
AUTH0_DOMAIN = 'dev-pnpogkrkp7l1bdda.us.auth0.com'  # Reemplaza con tu dominio de Auth0
CLIENT_ID = 'rjUUNTLgqkhwpW4u1WmRO6JxQ33WI0x2'      # Reemplaza con tu Client ID de la Aplicación Nativa
REDIRECT_URI = 'http://localhost:8000/callback'
AUDIENCE = 'https://users/api'
NAMESPACE = 'https://ofipensiones.com/claims/'      # Debe coincidir con el namespace en la acción personalizada

# Configuración de RabbitMQ
RABBITMQ_HOST = '10.128.0.4'       # Reemplaza con tu host de RabbitMQ
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'monitoring_user'
RABBITMQ_PASSWORD = 'isis2503'
RABBITMQ_EXCHANGE = 'bus_mensajeria'

# Variable global para almacenar el token
access_token = None

def get_jwks():
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def get_public_key(token):
    unverified_header = jwt.get_unverified_header(token)
    jwks = get_jwks()
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            return {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    return None

def decode_jwt(token):
    try:
        rsa_key = get_public_key(token)
        if not rsa_key:
            logging.error("No se pudo encontrar la clave RSA apropiada.")
            return None

        decoded = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return decoded
    except ExpiredSignatureError:
        logging.error("El token ha expirado.")
    except JWTError as e:
        logging.error(f"Error al decodificar el token: {e}")
    return None

def authenticate():
    global access_token
    session = OAuth2Session(
        CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope='openid profile email'
    )

    authorization_url, state = session.create_authorization_url(
        f'https://{AUTH0_DOMAIN}/authorize',
        audience=AUDIENCE,
        code_challenge_method='S256'
    )

    logging.info("Abriendo el navegador para autenticación...")
    webbrowser.open(authorization_url)

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            global access_token
            if self.path.startswith('/callback'):
                from urllib.parse import urlparse, parse_qs
                query = urlparse(self.path).query
                params = parse_qs(query)
                code = params.get('code')
                if code:
                    code = code[0]
                    try:
                        token = session.fetch_token(
                            f'https://{AUTH0_DOMAIN}/oauth/token',
                            code=code,
                            client_secret='RpgjMYB54Q5YXjWJwnAEqeRzpYdhf_LDH6VCVkTIxGz9kdWXj9GtdOOukvhoYuLU'  # Asegúrate de configurar esta variable
                        )
                        access_token = token.get('access_token')
                        logging.info("Autenticación exitosa. Token obtenido.")
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'Autenticacion exitosa. Puedes cerrar esta ventana.')
                        threading.Thread(target=self.server.shutdown).start()
                    except Exception as e:
                        logging.error(f"Error al intercambiar el código por token: {e}")
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b'Error durante la autenticacion.')
                else:
                    logging.error("No se encontró el código de autorización en la URL.")
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write('No se encontró el código de autorización.'.encode('utf-8'))

        def log_message(self, format, *args):
            return  # Evitar logs de HTTPServer en la consola

    server = HTTPServer(('localhost', 8000), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # Esperar hasta que el token sea obtenido
    while access_token is None:
        pass

def send_message_to_queue(queue, message):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/', credentials))
        channel = connection.channel()

        # Declarar el exchange si no existe
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct', durable=True)

        # Publicar el mensaje
        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=queue,
            body=json.dumps(message)
        )

        logging.info(f"Mensaje enviado a la cola '{queue}': {message}")
        connection.close()
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")

def main():
    # Autenticar al usuario
    authenticate()
    if not access_token:
        logging.error("No se pudo obtener el token de acceso. Saliendo del programa.")
        return

    # Decodificar el token
    decoded = decode_jwt(access_token)
    if not decoded:
        logging.error("No se pudo decodificar el token. Saliendo del programa.")
        return

    roles = decoded.get(f"{NAMESPACE}roles", [])
    user_id = decoded.get("sub", "unknown")

    logging.info(f"Roles obtenidos: {roles}, User ID: {user_id}")

    # Ejemplo de datos de usuarios para enviar a RabbitMQ
    usuarios = [
        {"action": "create", "user_id": "auth0|12345", "name": "Juan", "email": "juan@example.com"},
        {"action": "create", "user_id": "auth0|67890", "name": "Ana", "email": "ana@example.com"}
    ]

    for usuario in usuarios:
        # Validar acceso según rol
        if "Administrador" in roles:
            send_message_to_queue("admin.create", usuario)
        elif "Padre" in roles and usuario.get("user_id") == user_id:
            send_message_to_queue("parent.create", usuario)
        else:
            logging.warning(f"Acceso denegado para el usuario con roles {roles}: {usuario}")

if __name__ == "__main__":
    main()
