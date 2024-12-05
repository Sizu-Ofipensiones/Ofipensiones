import os
import json
import logging
import requests
import time
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pika
from jose import jwt, JWTError, ExpiredSignatureError
from authlib.integrations.requests_client import OAuth2Session

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuración de Auth0
AUTH0_DOMAIN = 'dev-pnpogkrkp7l1bdda.us.auth0.com'  # Reemplaza con tu dominio de Auth0
CLIENT_ID = 'rjUUNTLgqkhwpW4u1WmRO6JxQ33WI0x2'      # Reemplaza con tu Client ID de la Aplicación
CLIENT_SECRET = 'RpgjMYB54Q5YXjWJwnAEqeRzpYdhf_LDH6VCVkTIxGz9kdWXj9GtdOOukvhoYuLU'  # Configura esta variable de entorno
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

def device_authorization():
    url = f'https://{AUTH0_DOMAIN}/oauth/device/code'
    payload = {
        'client_id': CLIENT_ID,
        'scope': 'openid profile email',
        'audience': AUDIENCE
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def poll_for_token(device_code, interval, expires_in):
    global access_token
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET  # Asegúrate de que esta variable esté configurada
    }
    headers = {
        'Content-Type': 'application/json'
    }

    start_time = time.time()
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                logging.info("Autenticación exitosa. Token obtenido.")
                return
            else:
                error = response.json().get('error')
                if error == 'authorization_pending':
                    logging.info("Esperando a que el usuario autorice...")
                elif error == 'slow_down':
                    interval += 5
                    logging.info(f"Reduciendo la velocidad de polling. Nuevo intervalo: {interval} segundos.")
                elif error == 'expired_token':
                    logging.error("El token ha expirado. Intenta nuevamente.")
                    return
                elif error == 'access_denied':
                    logging.error("El acceso fue denegado por el usuario.")
                    return
                else:
                    logging.error(f"Error inesperado: {error}")
                    return
        except Exception as e:
            logging.error(f"Error durante el polling: {e}")
            return

        time.sleep(interval)
        if time.time() - start_time > expires_in:
            logging.error("Tiempo de espera agotado. No se obtuvo el token.")
            return

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
    global access_token

    # Paso 1: Iniciar el Device Authorization Flow
    device_code_response = device_authorization()
    device_code = device_code_response['device_code']
    user_code = device_code_response['user_code']
    verification_uri = device_code_response['verification_uri']
    verification_uri_complete = device_code_response.get('verification_uri_complete', verification_uri)
    expires_in = device_code_response['expires_in']
    interval = device_code_response['interval']

    # Mostrar instrucciones al usuario
    logging.info("Por favor, abre la siguiente URL en tu navegador y proporciona el código de usuario para autorizar la aplicación:")
    logging.info(f"URL: {verification_uri_complete}")
    logging.info(f"Código de Usuario: {user_code}")

    # Paso 2: Polling para obtener el token
    poll_for_token(device_code, interval, expires_in)

    if not access_token:
        logging.error("No se pudo obtener el token de acceso. Saliendo del programa.")
        return

    # Paso 3: Decodificar el token para obtener los roles
    decoded = decode_jwt(access_token)
    if not decoded:
        logging.error("No se pudo decodificar el token. Saliendo del programa.")
        return

    roles = decoded.get(f"{NAMESPACE}roles", [])
    user_id = decoded.get("sub", "unknown")

    logging.info(f"Roles obtenidos: {roles}, User ID: {user_id}")

    # Paso 4: Definir los datos a enviar
    # Puedes adaptar esta parte según tus necesidades específicas
    usuarios = [
        {"action": "create", "user_id": "auth0|12345", "name": "Juan", "email": "juan@example.com"},
        {"action": "create", "user_id": "auth0|67890", "name": "Ana", "email": "ana@example.com"}
    ]

    # Paso 5: Enviar mensajes a RabbitMQ basados en roles
    for usuario in usuarios:
        if "Administrador" in roles:
            send_message_to_queue("admin.create", usuario)
        elif "Padre" in roles and usuario.get("user_id") == user_id:
            send_message_to_queue("parent.create", usuario)
        else:
            logging.warning(f"Acceso denegado para el usuario con roles {roles}: {usuario}")

if __name__ == "__main__":
    main()