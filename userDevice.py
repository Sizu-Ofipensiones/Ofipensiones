import requests

# Configuración para Auth0
AUTH0_DOMAIN = 'dev-xitt1wu7afthncmv.us.auth0.com'
CLIENT_ID = 'hSLozg1PfmzHJa21LLAegsnLEq2jp1uf'
CLIENT_SECRET = '6DJJx9_TNCKVsXQColf6Q1q4SzhXxmoCeg2PidVCtGhVbT0eTvRwAdVntg6IVrhv'
AUDIENCE = 'https://users/api'
SCOPE = 'openid profile email'

def authenticate_user(username, password):
    """Autenticar usuario y obtener access token."""
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'audience': AUDIENCE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    if response.status_code == 200:
        print("Autenticación exitosa")
        return response_data.get('access_token')
    else:
        print(f"Error al autenticar: {response_data.get('error_description')}")
        return None

def get_user_details(access_token):
    """Obtener detalles del usuario usando el access token."""
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    userinfo = response.json()
    
    if response.status_code == 200:
        print("Información del usuario obtenida exitosamente")
        return userinfo
    else:
        print(f"Error al obtener información del usuario: {response.text}")
        return None

def get_user_role(access_token):
    """Obtener el rol del usuario desde el token."""
    userinfo = get_user_details(access_token)
    
    if userinfo:
        # Asegúrate de que el claim de rol esté presente en el token
        role_claim = f"https://{AUTH0_DOMAIN}/roles"
        role = userinfo.get(role_claim, "Sin rol asignado")
        print(f"Rol del usuario: {role}")
        return role
    return None

if __name__ == "__main__":
    # Solicitar credenciales al usuario
    username = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")

    # Autenticar usuario
    token = authenticate_user(username, password)
    
    if token:
        # Obtener y mostrar el rol del usuario
        get_user_role(token)
