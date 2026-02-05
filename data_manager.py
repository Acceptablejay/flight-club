import os
from dotenv import load_dotenv
from network import get_tls12_session

# load variables from .env file
load_dotenv()
BASIC_KEY = os.getenv("BASIC_KEY")

headers = {
                "Content-Type": "application/json",
                "Authorization": BASIC_KEY,
            }
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/b3890d6367f62b8d2568e931b76eb133/flightDeals/sheet1"

class DataManager:

    def __init__(self):
        self.session = get_tls12_session()
        self.destination_data = {}

    def get_destination_data(self):
        # Gets all the data from sheety, calls the actual sheet with the prices, in this case "sheet1"
        response = self.session.get(url=SHEETY_PRICES_ENDPOINT,headers=headers, timeout=30)
        data = response.json()
        self.destination_data = data["sheet1"]
        return self.destination_data

    #uses the row id to upate the iata codes and push the changes to sheety
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "sheet1": {
                    "iataCode": city["iataCode"]
                }
            }
            response = self.session.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=headers
            )
            print(response.text)