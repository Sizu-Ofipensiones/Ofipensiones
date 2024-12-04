import requests
from social_core.backends.oauth import BaseOAuth2

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    def authorization_url(self):
        """Return the authorization endpoint."""
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        """Return the token endpoint."""
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        return {
            'username': userinfo['nickname'],
            'first_name': userinfo['name'],
            'picture': userinfo['picture'],
            'user_id': userinfo['sub']
        }

# Función para obtener el rol del usuario
def getRole(request):
    user = request.user
    if not user.is_authenticated:
        return None
    auth0user = user.social_auth.filter(provider="auth0").first()
    if not auth0user:
        return None
    accessToken = auth0user.extra_data['access_token']
    url = "https://dev-pnpogkrkp7l1bdda.us.auth0.com/userinfo"
    headers = {'authorization': 'Bearer ' + accessToken}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        userinfo = resp.json()
        role = userinfo.get('dev-pnpogkrkp7l1bdda.us.auth0.com/role')
        return role
    except requests.exceptions.RequestException as e:
        # Manejar el error de la solicitud HTTP
        print(f"Error al obtener el rol del usuario: {e}")
        return None
