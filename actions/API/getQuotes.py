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

# Example usage
if __name__ == "__main__":
    api = QuotesAPI(
        base_url="https://dispatch.local.goodjourney.io/api/demand/v1/quotes",
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbGVldElkIjoieWVsbG93IiwidGhpcmRQYXJ0eSI6IlZpbmNlbnQgQVBJIiwiYXBwTmFtZSI6IlZpbmNlbnQgQVBJIiwiX2lkIjoiNjU5NzgwMjQ1YTNmMmI0YzAyOGU1ZjlkIiwiaWF0IjoxNzI1OTM4NTE1LCJleHAiOjE3MjU5NDIxMTUsImF1ZCI6ImF1dGguZ29qby5nbG9iYWwifQ.Ne3XITydRDEk76US-pDAFrROghaNUqepZaiXHiqVUrw"  # Replace with your token
    )
    
    pickup_datetime = "2024-09-10T12:06:14Z"
    pickup_coords = { "latitude": 16.059052,"longitude": 108.2112656,}
    destination_coords = { "latitude": 16.0595717,"longitude": 108.2111016,}
    
    # Call the API
    result = api.get_quotes(pickup_datetime, pickup_coords, destination_coords)
    
    # Print the result
    print(result)
