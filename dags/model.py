import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Date

class Connection(object):

    def __init__(self, db_connection):
        engine = create_engine(db_connection)
        self.engine = engine

    def get_session(self):
        Session = sessionmaker(bind=self.engine)

        return Session()

    def get_engine(self):
        return self.engine


Base = declarative_base()


def init_db(db_connection):
    engine = create_engine(db_connection)
    Base.metadata.create_all(bind=engine)

class OpenMeteo(Base):
    __tablename__ = 'openmeteo'

    key = Column(String, primary_key = True)
    date = Column(DateTime)
    temperature_2m = Column(Float)
    relative_humidity_2m = Column(Float)
    dew_point_2m = Column(Float)
    apparent_temperature = Column(Float)
    precipitation_probability = Column(Float)
    precipitation = Column(Float)
    rain = Column(Float)
    showers = Column(Float)
    snowfall = Column(Float)
    cloud_cover = Column(Float)
    visibility = Column(Float)
    wind_speed_10m = Column(Float)
    wind_direction_10m = Column(Float)
    uv_index = Column(Float)
    uv_index_clear_sky = Column(Float)
    is_day = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, key, date, temperature_2m, relative_humidity_2m, dew_point_2m,
                apparent_temperature, precipitation_probability, precipitation, rain, showers, snowfall,
                cloud_cover, visibility, wind_speed_10m, wind_direction_10m, uv_index, uv_index_clear_sky,
                is_day, location, latitude, longitude):
        self.key = key
        self.date = date
        self.temperature_2m = temperature_2m
        self.relative_humidity_2m = relative_humidity_2m
        self.dew_point_2m = dew_point_2m
        self.apparent_temperature = apparent_temperature
        self.precipitation_probability = precipitation_probability
        self.precipitation = precipitation
        self.rain = rain
        self.showers = showers
        self.snowfall = snowfall
        self.cloud_cover = cloud_cover
        self.visibility = visibility
        self.wind_speed_10m = wind_speed_10m
        self.wind_direction_10m = wind_direction_10m
        self.uv_index = uv_index
        self.uv_index_clear_sky =  uv_index_clear_sky
        self.is_day = is_day
        self.location = location
        self.latitude = latitude
        self.longitude = longitude