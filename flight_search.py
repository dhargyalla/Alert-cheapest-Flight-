import os

import requests
from datetime import datetime

flight_auth_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
flight_endpoint ="https://test.api.amadeus.com/v2/shopping/flight-offers"
IATA_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):

        self.client_id = os.environ["AMADEUS_API_KEY"]
        self.client_secret = os.environ["AMADEUS_SECRET"]
        self.TOKEN = self.authorization()
        self.origin = "PAR"
        self.maxPrice = 200


    def authorization(self):

        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        auth_params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'client_credentials',
        }
        response = requests.post(url=flight_auth_endpoint, data =auth_params, headers=header)
        access_token = response.json()['access_token']
        return access_token

    # def flight_data(self):
    #     # Set Authorization Header with Bearer Token
    #     self.flight_headers = {
    #         "Authorization": f"Bearer {self.TOKEN}",
    #         "Content-Type": "application/json"
    #     }
    #
    #     self.flight_params = {
    #         "origin": self.origin,
    #         "maxPrice": self.maxPrice,
    #     }
    #
    #     self.response = requests.get(url=flight_endpoint, params=self.flight_params, headers=self.flight_headers)
    #     # print(self.response.json())
    #     # print(self.response.text)

    def get_destination_code(self, city_name):
        # Return "TESTING" for now to make sure Sheety is working. Get TEQUILA API data later.
        print(f"Using this token to get destination {self.TOKEN}")
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=IATA_endpoint,
            headers=headers,
            params=query
        )

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """
        Searches for flight options between two cities on specified departure and return dates
        using the Amadeus API.
        Parameters:
            origin_city_code (str): The IATA code of the departure city.
            destination_city_code (str): The IATA code of the destination city.
            from_time (datetime): The departure date.
            to_time (datetime): The return date.
        Returns:
            dict or None: A dictionary containing flight offer data if the query is successful; None
            if there is an error.
        The function constructs a query with the flight search parameters and sends a GET request to
        the API. It handles the response, checking the status code and parsing the JSON data if the
        request is successful. If the response status code is not 200, it logs an error message and
        provides a link to the API documentation for status code details.
        """

        # print(f"Using this token to check_flights() {self._token}")
        headers = {"Authorization": f"Bearer {self.TOKEN}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=flight_endpoint,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()