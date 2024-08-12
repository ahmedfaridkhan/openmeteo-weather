import argparse
import os
import csv
from datetime import timedelta, datetime

from model import Connection, OpenMeteo
import config
from sqlalchemy.dialects.postgresql import insert

def get_date_range(fetch_date):
    start_date = datetime.strptime(fetch_date, '%Y-%m-%d').date()
    end_date = start_date + timedelta(days=6)
    return start_date, end_date

def get_file_path(fetch_date):
    start_date, _ = get_date_range(fetch_date)
    filename = "openmeteo_{}_to_{}.csv".format(start_date, start_date + timedelta(days=6))
    return os.path.join(config.CSV_FILE_DIR, filename)

def main(fetch_date, db_connection):
    today = datetime.strptime(fetch_date, '%Y-%m-%d').date()
    filename = get_file_path(fetch_date)
    data_insert = []

    with open(filename, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            openmeteo_data = {
                'key': row['key'],
                'date': row['date'],
                'temperature_2m': row['temperature_2m'],
                'relative_humidity_2m': row['relative_humidity_2m'],
                'dew_point_2m': row['dew_point_2m'],
                'apparent_temperature': row['apparent_temperature'],
                'precipitation_probability': row['precipitation_probability'],
                'precipitation': row['precipitation'],
                'rain': row['rain'],
                'showers': row['showers'],
                'snowfall': row['snowfall'],
                'cloud_cover': row['cloud_cover'],
                'visibility': row['visibility'],
                'wind_speed_10m': row['wind_speed_10m'],
                'wind_direction_10m': row['wind_direction_10m'],
                'uv_index': row['uv_index'],
                'uv_index_clear_sky': row['uv_index_clear_sky'],
                'is_day': row['is_day'],
                'location': row['location'],
                'latitude': row['latitude'],
                'longitude': row['longitude']
            }
            data_insert.append(openmeteo_data)

    connection = Connection(db_connection)
    session = connection.get_session()

    # Use ON CONFLICT to update existing records
    stmt = insert(OpenMeteo).values(data_insert)
    update_columns = {
        'date': stmt.excluded.date,
        'temperature_2m': stmt.excluded.temperature_2m,
        'relative_humidity_2m': stmt.excluded.relative_humidity_2m,
        'dew_point_2m': stmt.excluded.dew_point_2m,
        'apparent_temperature': stmt.excluded.apparent_temperature,
        'precipitation_probability': stmt.excluded.precipitation_probability,
        'precipitation': stmt.excluded.precipitation,
        'rain': stmt.excluded.rain,
        'showers': stmt.excluded.showers,
        'snowfall': stmt.excluded.snowfall,
        'cloud_cover': stmt.excluded.cloud_cover,
        'visibility': stmt.excluded.visibility,
        'wind_speed_10m': stmt.excluded.wind_speed_10m,
        'wind_direction_10m': stmt.excluded.wind_direction_10m,
        'uv_index': stmt.excluded.uv_index,
        'uv_index_clear_sky': stmt.excluded.uv_index_clear_sky,
        'is_day': stmt.excluded.is_day,
        'location': stmt.excluded.location,
        'latitude': stmt.excluded.latitude,
        'longitude': stmt.excluded.longitude
    }
    stmt = stmt.on_conflict_do_update(index_elements=['key'], set_=update_columns)

    session.execute(stmt)
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, type=str)
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.date, args.connection)
