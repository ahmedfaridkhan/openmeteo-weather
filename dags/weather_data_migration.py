import argparse
from pathlib import Path

from model import Connection
import config

#Initialize table
def main(db_connection):
    Path(config.CSV_FILE_DIR).mkdir(parents=True, exist_ok=True)

    connection = Connection(db_connection)
    session = connection.get_session()
    session.execute('''CREATE TABLE IF NOT EXISTS openmeteo (
    key VARCHAR PRIMARY KEY,
    date TIMESTAMP,
    temperature_2m DECIMAL,
    relative_humidity_2m DECIMAL,
    dew_point_2m DECIMAL,
    apparent_temperature DECIMAL,
    precipitation_probability DECIMAL,
    precipitation DECIMAL,
    rain DECIMAL,
    showers DECIMAL,
    snowfall DECIMAL,
    cloud_cover DECIMAL,
    visibility DECIMAL,
    wind_speed_10m DECIMAL,
    wind_direction_10m DECIMAL,
    uv_index DECIMAL,
    uv_index_clear_sky DECIMAL,
    is_day DECIMAL,
    location VARCHAR,
    latitude DECIMAL,
    longitude DECIMAL )''')
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.connection)