import requests
import xml.etree.ElementTree as ElementTree
from dotenv import load_dotenv
import os

class Client:
    def __init__(self) -> None:
        self.get_environment_variables()

    def get_environment_variables(self):
        load_dotenv()
        self._api_url = os.getenv("API_URL")
    
    def fetch_data(self) -> str:
        try:
            response = requests.get(self._api_url)
            payload = ""
            statusCode = response.status_code
            if response.status_code == 200:
                payload = response.text
                print("API_CLIENT: Fetched data succesfully")
            else:
                print(f"API_CLIENT: Failed to fetch data with {statusCode}")
            return payload
        except Exception as error:
            print(f"API_CLIENT: Failed to request with {error}")

    def parse_data(self) -> ElementTree:
        response  = self.fetch_data()
        try:
            root = ElementTree.fromstring(response)
            print(root)
            return root

        except ElementTree.ParseError as error:
            print(f"API_CLIENT: Error parsing XML: {error}")
    
    def extract_data(self) -> dict:
        root = self.parse_data()

    def get_data(self):
        pass