import requests
from flask import current_app
from app.services.auth_service import auth_service
from app.utils.exceptions import ProveAPIError

class ProveService:
    def __init__(self):
        self.base_url = None

    def _get_config(self):
        """Get configuration from Flask app"""
        if not self.base_url:
            self.base_url = current_app.config['PROVE_API_BASE_URL']

    def _get_headers(self) -> dict:
        """Get headers for Prove API requests"""
        token = auth_service.get_oauth_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def start_flow(self, phone_number: str, flow_type: str, ssn: str) -> dict:
        """Start the flow"""
        self._get_config()

        url = f"{self.base_url}/v3/start"

        headers = self._get_headers()

        data = {
            'phoneNumber': phone_number,
            'flowType': flow_type,
            'finalTargetUrl': "https://www.example.com/landing-page",
            'ssn': ssn
        }

        try:
            response = requests.post(url=url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error starting flow: {e}")
            raise ProveAPIError(f"Failed to start verification: {str(e)}")
        
    def validate_phone_number(self, correlation_id: str) -> dict:
        """Check if the phone number entered/discovered earlier in the flow is validated"""
        self._get_config()

        url = f"{self.base_url}/v3/validate"

        headers = self._get_headers()

        data = {
            'correlationId': correlation_id
        }

        try:
            response = requests.post(url=url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error validating phone number: {e}")
            raise ProveAPIError(f"Failed to validate phone number: {str(e)}")
        
    def complete_flow(self, correlation_id: str, user_data: dict) -> dict:
        """Verify the user and complete the flow"""
        self._get_config()

        url = f"{self.base_url}/v3/complete"

        headers = self._get_headers()

        data = {
            'correlationId': correlation_id,
            'individual': user_data
        }

        try:
            response = requests.post(url=url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error completing flow: {e}")
            raise ProveAPIError(f"Failed to complete verification: {str(e)}")


# Global prove service instance
prove_service = ProveService()