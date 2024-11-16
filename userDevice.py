from authlib.integrations.requests_client import OAuth2Session
import os
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Configuración de Auth0
AUTH0_DOMAIN = 'dev-pnpogkrkp7l1bdda.us.auth0.com'
CLIENT_ID = 'rjUUNTLgqkhwpW4u1WmRO6JxQ33WI0x2'  # Client ID de la Aplicación Nativa
REDIRECT_URI = 'http://localhost:8000/callback'
AUDIENCE = 'https://users/api'

# Crear una sesión OAuth2 con PKCE
session = OAuth2Session(
    CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope='openid profile email'
)

# Generar la URL de autorización
authorization_url, state = session.create_authorization_url(
    f'https://{AUTH0_DOMAIN}/authorize',
    audience=AUDIENCE,
    code_challenge_method='S256'
)

# Abrir el navegador para que el usuario inicie sesión
webbrowser.open(authorization_url)

# Variable global para almacenar el token
access_token = None

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Servidor HTTP para manejar el callback
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token
        if self.path.startswith('/callback'):
            # Extraer el código de autorización
            from urllib.parse import urlparse, parse_qs
            query = urlparse(self.path).query
            params = parse_qs(query)
            code = params.get('code')[0]
            
            try:
                # Intercambiar el código por un token
                token = session.fetch_token(
                    f'https://{AUTH0_DOMAIN}/oauth/token',
                    code=code,
                    client_secret='RpgjMYB54Q5YXjWJwnAEqeRzpYdhf_LDH6VCVkTIxGz9kdWXj9GtdOOukvhoYuLU'# Asegúrate de configurar esta variable
                )
                access_token = token['access_token']
                logging.info("Autenticación exitosa. Token obtenido.")
                
                # Responder al usuario
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Autenticación exitosa. Puedes cerrar esta ventana.')
                
                # Detener el servidor
                threading.Thread(target=self.server.shutdown).start()
            except Exception as e:
                logging.error(f"Error al intercambiar el código por token: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error durante la autenticación.')
                
    def log_message(self, format, *args):
        return  # Evitar logs de HTTPServer en la consola

# Iniciar el servidor HTTP
server = HTTPServer(('localhost', 8000), CallbackHandler)
server.serve_forever()

# Ahora puedes usar el access_token
if access_token:
    print(f'Token de acceso: {access_token}')
    # Continúa con la lógica para enviar mensajes a RabbitMQ usando el access_token
else:
    print("No se obtuvo el token de acceso.")
