from sqlmodel import Field, SQLModel, Session, create_engine, Relationship, select
from datetime import datetime
from dotenv import load_dotenv
import os


class Station(SQLModel, table=True):
    station_id: int = Field(default=None, primary_key=True)
    station_name: str
    lat: float
    lon: float
    region: str

    measurements: list["Measurement"] = Relationship(back_populates="station")

class Measurement(SQLModel, table=True):
    measurement_id: int = Field(default=None, primary_key=True)
    station_id: int = Field(foreign_key="station.station_id")
    timestamp: datetime
    temperature: float = None
    ground_temperature: float = None
    feel_temperature: float = None
    wind_gusts: float = None
    wind_speed: float = None
    precitipation: float = None
    sun_power: float = None

    station: Station = Relationship(back_populates="measurements")

class Client():
    def __init__(self) -> None:
        self.get_environment_variables()
        self.start_database_engine()

    def get_environment_variables(self):
        load_dotenv()
        self._db_url = os.getenv("DATABASE_URL")
    
    def start_database_engine(self):
        self._db_engine = create_engine(self._db_url, echo=True)
        SQLModel.metadata.create_all(self._db_engine)
    
    def setup_session(self) -> Session:
        with Session(self._db_engine) as session:
            return session

    def add_station(
            self,
            station_name: str,
            lat: float,
            lon: float,
            region: str
        ):
        with self.setup_session() as session:
            station = Station(
                station_name=station_name,
                lat=lat,
                lon=lon,
                region=
                region
                )
            session.add(station)
            session.commit()

    def add_measurement(
            self,
            station_id: int,
            timestamp: datetime,
            temperature: float,
            ground_temperature: float,
            feel_temperature: float,
            wind_gusts: float,
            wind_speed: float,
            precitipation: float,
            sun_power: float
        ):  
        with self.setup_session() as session:
            measurement = Measurement(
                station_id=station_id,
                timestamp=timestamp,
                temperature=temperature,
                ground_temperature=ground_temperature,
                feel_temperature=feel_temperature,
                wind_gusts=wind_gusts,
                wind_speed=wind_speed,
                precitipation=precitipation,
                sun_power=sun_power
            )
            session.add(measurement)
            session.commit()

    def query_all_instances(self):
        with self.setup_session() as session:
            stations = session.exec(select(Station)).all()
            for station in stations:
                print(f"{station.station_name}: \n")
                measurements = session.exec(select(Measurement).where(Measurement.station_id==station.station_id)).all()
                for measurement in measurements:
                    print(f"- {measurement.measurement_id} \n")