import pika
import json
import requests

# Configuración de Auth0
AUTH0_DOMAIN = 'dev-xitt1wu7afthncmv.us.auth0.com'
CLIENT_ID = 'TTmqAS6niW6L9heQPuNX650m7wLrHWpk'
CLIENT_SECRET = 'tTRaEYXFEgtKYW3xCGVVxCCTgcJp_elcfoPaISz4M7L_EkIX-Fbg-1Fg51wR7rj6'
AUDIENCE = 'https/users/api'

def authenticate_user():
    """
    Solicitar credenciales al usuario y autenticarse en Auth0.
    """
    print("\n=== Iniciar Sesión en el Sistema ===")
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

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        token = data.get('access_token')

        if token:
            print("Autenticación exitosa")
            return token
        else:
            print("No se pudo obtener el token.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al autenticar: {e}")
        return None

def get_user_roles(token):
    """
    Recupera los roles del usuario autenticado desde el token JWT.
    """
    # Verificar los roles directamente desde el token
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        roles = user_data.get("https://example.com/roles", [])  # Ajusta según la configuración del claim en Auth0
        user_id = user_data.get("sub", "unknown")

        return roles, user_id
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener roles: {e}")
        return [], "unknown"

def send_message_to_queue(queue, message, roles, user_id):
    """
    Envía un mensaje a RabbitMQ validando los roles primero.
    """
    # Validar acceso según rol
    if "Administrador" in roles:
        print("Acceso concedido: Administrador")
    elif "Padre" in roles and message.get("user_id") == user_id:
        print("Acceso concedido: Padre")
    else:
        print("Acceso denegado.")
        return

    # Conectar con RabbitMQ
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Publicar el mensaje
    channel.basic_publish(
        exchange='bus_mensajeria',
        routing_key=queue,
        body=json.dumps(message)
    )

    print(f"Mensaje enviado a {queue}: {message}")
    connection.close()

def main():
    # Autenticar al usuario
    token = authenticate_user()
    if not token:
        print("No se pudo autenticar al usuario. Saliendo.")
        return

    # Obtener roles e ID del usuario
    roles, user_id = get_user_roles(token)
    print(f"Roles: {roles}, User ID: {user_id}")


    for usuario in usuarios:
        send_message_to_queue("user.create", usuario, roles, user_id)

if __name__ == "__main__":
    main()
