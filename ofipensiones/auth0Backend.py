import logging
import requests
from social_core.backends.oauth import BaseOAuth2

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Para imprimir en la consola
    ]
)

logger = logging.getLogger(__name__)

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
        url = "https://" + self.setting('DOMAIN') + "/authorize"
        logger.debug(f"Authorization URL: {url}")
        return url

    def access_token_url(self):
        """Return the token endpoint."""
        url = "https://" + self.setting('DOMAIN') + "/oauth/token"
        logger.debug(f"Access token URL: {url}")
        return url

    def get_user_id(self, details, response):
        """Return current user id."""
        user_id = details['user_id']
        logger.info(f"User ID retrieved: {user_id}")
        return user_id

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        logger.debug(f"Fetching user details from: {url}")
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            userinfo = resp.json()
            logger.info("User details fetched successfully")
            return {
                'username': userinfo['nickname'],
                'first_name': userinfo['name'],
                'picture': userinfo['picture'],
                'user_id': userinfo['sub']
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user details: {e}")
            return {}


