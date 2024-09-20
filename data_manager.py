import requests
from pprint import pprint
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os

# Load environment variables from .env file
load_dotenv()

sheety_endpoint = "https://api.sheety.co/60e6a1cf96538fef5c458a92059b2135/copyOfFlightDeals/prices"

class DataManager:
    def __init__(self):
        self._user = os.environ['SHEETY_USERNAME']
        self._password = os.environ['SHEETY_PASSWORD']
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_endpoint,auth=self._authorization)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheety_endpoint}/{city['id']}",
                json=new_data,
                auth=self._authorization,
            )
            print(response.text)