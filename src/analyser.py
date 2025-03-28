import database
import api

class Analyser:
    def __init__(self) -> None:
        self._db_client = database.Client()
        self._db_client.query_all_instances()
        self._api_client  = api.Client()

    def insert_data(self):
        data = self._api_client.get_data()
        feelTemprature = lambda  temperature, windSpeed, humidity: (13.12 + 0.6215 * temperature - 11.37 * (windSpeed ** 0.16) + 0.3965 * temperature * (windSpeed ** 0.16)
            if windSpeed is not None and windSpeed > 0 else  # Wind Chill only applies if wind speed is provided
            (-8.78469475556 + 1.61139411 * temperature + 2.33854883889 * humidity - 0.14611605 * temperature * humidity - 0.012308094 * temperature**2 
            - 0.0164248277778 * humidity**2 + 0.002211732 * temperature**2 * humidity + 0.00072546 * temperature * humidity**2 - 0.000003582 * temperature**2 * humidity**2) 
        )   
        for station in data["stations"]:
            self._db_client.add_station(
                station_id=station["station_id"],
                station_name=station["station_name"],
                lat=station["lat"],
                lon=station["lon"],
                region=station["region"]
            )
        for measurement in data["measurements"]:
            self._db_client.add_measurement(
                station_id = measurement["station_id"],
                timestamp = measurement["timestamp"],
                temperature = measurement["temperature"],
                ground_temperature = measurement["ground_temperature"],
                feel_temperature = feelTemprature(measurement["temperature"], measurement["winds_speed"], measurement["humidity"]),
                wind_gusts = measurement["timestamp"],
                wind_speed = measurement["wind_speed"],
                precitipation = measurement["precitipation"],
                sun_power = measurement["sun_power"]
            )