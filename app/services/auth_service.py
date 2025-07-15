import requests
from flask import current_app
from app.services.cache_service import cache
from app.utils.exceptions import AuthenticationError

class AuthService:
    TOKEN_CACHE_KEY = 'prove_oauth_token'

    def __init__(self):
        self.base_url = None
        self.client_id = None
        self.client_secret = None

    def _get_config(self):
        """"Get configuration from Flask app"""
        if not self.base_url:
            self.base_url = current_app.config['PROVE_API_BASE_URL']
            self.client_id = current_app.config['PROVE_CLIENT_ID']
            self.client_secret = current_app.config['PROVE_CLIENT_SECRET']

    def get_oauth_token(self) -> str:
        """Get OAuth token with caching"""
        self._get_config()

        # Check cache first
        cached_token = cache.get(self.TOKEN_CACHE_KEY)
        if cached_token:
            return cached_token

        # If not cached, request a new token
        token_data = self._request_token()
        token = token_data['access_token']
        expires_in = token_data['expires_in']

        # Cache token with a 5 minute buffer
        cache.set(self.TOKEN_CACHE_KEY, token, expires_in - 300)

        return token

    def _request_token(self) -> dict:
        """Request OAuth token from Prove API"""
        url = f"{self.base_url}/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error requesting OAuth token: {e}")
            raise AuthenticationError(f"Failed to get OAuth token: {str(e)}")

# Global instance of AuthService
auth_service = AuthService()