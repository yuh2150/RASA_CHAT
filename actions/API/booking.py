import requests
import json

class BookingAPI:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
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

# Example usage
if __name__ == "__main__":
    # Initialize the BookingClient with the base URL and auth token
    booking_client = BookingAPI(
        base_url="https://dispatch.local.goodjourney.io/api/demand",
        auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbGVldElkIjoieWVsbG93IiwidGhpcmRQYXJ0eSI6IlZpbmNlbnQgQVBJIiwiYXBwTmFtZSI6IlZpbmNlbnQgQVBJIiwiX2lkIjoiNjU5NzgwMjQ1YTNmMmI0YzAyOGU1ZjlkIiwiaWF0IjoxNzI1OTM4NTE1LCJleHAiOjE3MjU5NDIxMTUsImF1ZCI6ImF1dGguZ29qby5nbG9iYWwifQ.Ne3XITydRDEk76US-pDAFrROghaNUqepZaiXHiqVUrw"  # Replace with your token
    )

    # Passenger details
    passenger_info = {
        "title": "Mr",
        "phone": "+120517347",
        "firstName": "Daid",
        "lastName": "James"
    }

    # Create booking request
    response = booking_client.create_booking(
        quote_id="b74438c8-e40e-472d-a9dc-170f3d2ca191",
        passenger_info=passenger_info
    )

    # Print the result
    print(response)
