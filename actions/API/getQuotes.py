import requests
import json

class QuotesAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def get_quotes(self, pickup_datetime, pickup_coords, destination_coords):
        payload = json.dumps({
            "pickupDateTime": pickup_datetime,
            "pickup": {
                "latitude": pickup_coords['latitude'],
                "longitude": pickup_coords['longitude'],
            },
            "destination": {
                "latitude": destination_coords['latitude'],
                "longitude": destination_coords['longitude'],
            },
        })

        try:
            response = requests.post(self.base_url, headers=self.headers, data=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error: {response.status_code}, {response.text}"}
        except requests.RequestException as e:
            return {"error": str(e)}
class Quote:
    def __init__(self, quote_id, expires_at, vehicle_type, price_value, price_currency, luggage, passengers, provider_name, provider_phone):
        self.quote_id = quote_id
        self.expires_at = expires_at
        self.vehicle_type = vehicle_type
        self.price_value = price_value
        self.price_currency = price_currency
        self.luggage = luggage
        self.passengers = passengers
        self.provider_name = provider_name
        self.provider_phone = provider_phone

    def __repr__(self):
        return (f"Quote(quote_id={self.quote_id}, expires_at={self.expires_at}, vehicle_type={self.vehicle_type}, "
                f"price_value={self.price_value}, price_currency={self.price_currency}, luggage={self.luggage}, "
                f"passengers={self.passengers}, provider_name={self.provider_name}, provider_phone={self.provider_phone})")
# Example usage
if __name__ == "__main__":
    api = QuotesAPI(
        base_url="https://dispatch.local.goodjourney.io/api/demand/v1/quotes",
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbGVldElkIjoieWVsbG93IiwidGhpcmRQYXJ0eSI6IlZpbmNlbnQgQVBJIiwiYXBwTmFtZSI6IlZpbmNlbnQgQVBJIiwiX2lkIjoiNjU5NzgwMjQ1YTNmMmI0YzAyOGU1ZjlkIiwiaWF0IjoxNzI2MTI3OTM0LCJleHAiOjE3MjYxMzE1MzQsImF1ZCI6ImF1dGguZ29qby5nbG9iYWwifQ.KvZEvG5yeAX9zMTA2be6SHrGdS_CpnFamCUnGU0rtfc"  # Replace with your token
    )
    
    pickup_datetime = "2024-10-12T15:06:14Z"
    pickup_coords = { "latitude": 16.059058,"longitude": 108.211266,}
    destination_coords = { "latitude": 16.0595717,"longitude": 108.2111016,}
    
    # Call the API
    result = api.get_quotes(pickup_datetime, pickup_coords, destination_coords)

    # Assuming result is now a list of dictionaries
    quotes = []
    for item in result:
        # Ensure item is a dictionary
        quote = Quote(
            quote_id=item['quoteId'],
            expires_at=item['expiresAt'],
            vehicle_type=item['vehicleType'],
            price_value=item['price']['value'],
            price_currency=item['price']['currency'],
            luggage=item['luggage'],
            passengers=item['passengers'],
            provider_name=item['provider']['name'],
            provider_phone=item['provider']['phone']
        )
        quotes.append(quote)


    # Print the result
    for q in quotes:
        print(q)

    print(result)
