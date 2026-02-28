import os
import requests
import base64

class PayPalService:
    
    def __init__(self):
        self.client_id = os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
        self.base_url = "https://api-m.sandbox.paypal.com"
    
    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, headers=headers, data={"grant_type": "client_credentials"}, timeout=10)
        if response.status_code == 200:
            return response.json()["access_token"]
        raise Exception(f"Error obteniendo token: {response.text}")
    
    def create_payment(self, amount, currency, description, return_url, cancel_url, solicitud_id=None):
        try:
            token = self.get_access_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            payload = {
                "intent": "CAPTURE",
                "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}, "description": description}],
                "application_context": {"return_url": return_url, "cancel_url": cancel_url, "brand_name": "UTNG - Laboratorio", "user_action": "PAY_NOW", "shipping_preference": "NO_SHIPPING"}
            }
            response = requests.post(f"{self.base_url}/v2/checkout/orders", json=payload, headers=headers, timeout=15)
            if response.status_code == 201:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {"error": str(e)}
    
    def capture_payment(self, order_id):
        try:
            token = self.get_access_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            response = requests.post(f"{self.base_url}/v2/checkout/orders/{order_id}/capture", headers=headers, timeout=15)
            if response.status_code == 201:
                return True, response.json()
            return False, response.json()
        except Exception as e:
            return False, {"error": str(e)}