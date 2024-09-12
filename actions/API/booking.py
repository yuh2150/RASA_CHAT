import requests
import json

class BookingAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def create_booking(self, quote_id, passenger_info):

        url = f"{self.base_url}/v1/bookings"
        payload = {
            "quoteId": quote_id,
            "passenger": passenger_info
        }

        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))

            if response.status_code == 200:
                return response.json()  # Successful response
            else:
                return {
                    "error": response.status_code,
                    "message": response.text
                }
        except requests.exceptions.RequestException as e:
            return {"error": "Request failed", "message": str(e)}


