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

    @property
    def get_data(self):
        self.parse_data()
    
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
            data = {
            "stations": {},
            "measurements": []
            }
            for station in root.findall(".//weerstation"):
                station_code = station.find("stationcode")
                if station_code is not None:
                    station_code = station_code.text
                else:
                    station_code = "Unknown"

                data["stations"][station_code] = {
                    "station_id": station_code,
                    "station_name": station.find("stationnaam").text if station.find("stationnaam") is not None else "Unknown",
                    "lat": station.find("lat").text if station.find("lat") is not None else "Unknown",
                    "lon": station.find("lon").text if station.find("lon") is not None else "Unknown",
                    "region": station.find("stationnaam").attrib if station.find("stationnaam") is not None else {}
                }

                measurement = {
                    "station_id": station_code,
                    "timestamp": station.find("datum").text if station.find("datum") is not None else "Unknown",
                    "temperature": station.find("temperatuur10cm").text if station.find("temperatuur10cm") is not None else "Unknown",
                    "ground_temperature": station.find("tempratuurGC").text if station.find("tempratuurGC") is not None else "Unknown",
                    "wind_gusts": station.find("windstotenMS").text if station.find("windstotenMS") is not None else "Unknown",
                    "wind_speed": station.find("windsnelheidMS").text if station.find("windsnelheidMS") is not None else "Unknown",
                    "precipitation": station.find("regenMMPU").text if station.find("regenMMPU") is not None else "Unknown",
                    "sun_power": station.find("zonintensieteit").text if station.find("zonintensieteit") is not None else "Unknown"
                }

                data["measurements"].append(measurement)

            return data
        except ElementTree.ParseError as error:
            print(f"API_CLIENT: Error parsing XML: {error}")
            return {}