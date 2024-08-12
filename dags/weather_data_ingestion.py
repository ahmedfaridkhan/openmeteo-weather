import requests
import openmeteo_requests
import argparse
import os

import requests_cache
from retry_requests import retry

from datetime import timedelta, datetime
import pandas as pd
import json

import config

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Function to retrieve weather details for a given latitude and longitude
def ingest_weather_data():
    cities = [
    {"city": "New York", "latitude": 40.71, "longitude": -74.01},
    {"city": "Los Angeles", "latitude": 34.05, "longitude": -118.24},
    {"city": "Chicago", "latitude": 41.88, "longitude": -87.63},
    {"city": "Houston", "latitude": 29.76, "longitude": -95.37},
    {"city": "Phoenix", "latitude": 33.45, "longitude": -112.07},
    {"city": "Philadelphia", "latitude": 39.95, "longitude": -75.17},
    {"city": "San Antonio", "latitude": 29.42, "longitude": -98.49},
    {"city": "San Diego", "latitude": 32.72, "longitude": -117.16},
    {"city": "Dallas", "latitude": 32.78, "longitude": -96.8},
    {"city": "San Jose", "latitude": 37.34, "longitude": -121.89},
    {"city": "Austin", "latitude": 30.27, "longitude": -97.74},
    {"city": "Jacksonville", "latitude": 30.33, "longitude": -81.65},
    {"city": "Fort Worth", "latitude": 32.75, "longitude": -97.33},
    {"city": "Columbus", "latitude": 39.96, "longitude": -83.0},
    {"city": "Charlotte", "latitude": 35.23, "longitude": -80.84},
    {"city": "San Francisco", "latitude": 37.77, "longitude": -122.42},
    {"city": "Indianapolis", "latitude": 39.77, "longitude": -86.16},
    {"city": "Seattle", "latitude": 47.61, "longitude": -122.33},
    {"city": "Denver", "latitude": 39.74, "longitude": -104.99},
    {"city": "Washington", "latitude": 38.91, "longitude": -77.04},
    {"city": "Boston", "latitude": 42.36, "longitude": -71.06},
    {"city": "El Paso", "latitude": 31.76, "longitude": -106.49},
    {"city": "Nashville", "latitude": 36.16, "longitude": -86.78},
    {"city": "Detroit", "latitude": 42.33, "longitude": -83.05},
    {"city": "Oklahoma City", "latitude": 35.47, "longitude": -97.52},
    {"city": "Portland", "latitude": 45.52, "longitude": -122.68},
    {"city": "Las Vegas", "latitude": 36.17, "longitude": -115.14},
    {"city": "Memphis", "latitude": 35.15, "longitude": -90.05},
    {"city": "Louisville", "latitude": 38.25, "longitude": -85.76},
    {"city": "Baltimore", "latitude": 39.29, "longitude": -76.61},
    {"city": "Milwaukee", "latitude": 43.04, "longitude": -87.91},
    {"city": "Albuquerque", "latitude": 35.08, "longitude": -106.65},
    {"city": "Tucson", "latitude": 32.22, "longitude": -110.97},
    {"city": "Fresno", "latitude": 36.73, "longitude": -119.79},
    {"city": "Mesa", "latitude": 33.42, "longitude": -111.83},
    {"city": "Sacramento", "latitude": 38.58, "longitude": -121.49},
    {"city": "Atlanta", "latitude": 33.75, "longitude": -84.39},
    {"city": "Kansas City", "latitude": 39.1, "longitude": -94.58},
    {"city": "Colorado Springs", "latitude": 38.83, "longitude": -104.82},
    {"city": "Miami", "latitude": 25.77, "longitude": -80.19},
    {"city": "Raleigh", "latitude": 35.78, "longitude": -78.64},
    {"city": "Omaha", "latitude": 41.26, "longitude": -95.94},
    {"city": "Long Beach", "latitude": 33.77, "longitude": -118.19},
    {"city": "Virginia Beach", "latitude": 36.85, "longitude": -75.98},
    {"city": "Oakland", "latitude": 37.8, "longitude": -122.27},
    {"city": "Minneapolis", "latitude": 44.98, "longitude": -93.27},
    {"city": "Tulsa", "latitude": 36.15, "longitude": -95.99},
    {"city": "Arlington", "latitude": 32.74, "longitude": -97.11},
    {"city": "Tampa", "latitude": 27.95, "longitude": -82.46},
    {"city": "New Orleans", "latitude": 29.95, "longitude": -90.07},
    {"city": "Wichita", "latitude": 37.69, "longitude": -97.34},
    {"city": "Cleveland", "latitude": 41.5, "longitude": -81.69},
    {"city": "Bakersfield", "latitude": 35.37, "longitude": -119.02},
    {"city": "Aurora", "latitude": 39.73, "longitude": -104.83},
    {"city": "Anaheim", "latitude": 33.83, "longitude": -117.91},
    {"city": "Honolulu", "latitude": 21.31, "longitude": -157.86},
    {"city": "Santa Ana", "latitude": 33.74, "longitude": -117.87},
    {"city": "Riverside", "latitude": 33.98, "longitude": -117.38},
    {"city": "Corpus Christi", "latitude": 27.8, "longitude": -97.4},
    {"city": "Lexington", "latitude": 38.04, "longitude": -84.5},
    {"city": "Stockton", "latitude": 37.96, "longitude": -121.29},
    {"city": "Henderson", "latitude": 36.04, "longitude": -115.05},
    {"city": "Saint Paul", "latitude": 44.95, "longitude": -93.1},
    {"city": "St. Louis", "latitude": 38.63, "longitude": -90.2},
    {"city": "Cincinnati", "latitude": 39.1, "longitude": -84.51},
    {"city": "Pittsburgh", "latitude": 40.44, "longitude": -79.99},
    {"city": "Greensboro", "latitude": 36.07, "longitude": -79.79},
    {"city": "Anchorage", "latitude": 61.22, "longitude": -149.89},
    {"city": "Plano", "latitude": 33.02, "longitude": -96.7},
    {"city": "Lincoln", "latitude": 40.81, "longitude": -96.68},
    {"city": "Orlando", "latitude": 28.54, "longitude": -81.38},
    {"city": "Irvine", "latitude": 33.68, "longitude": -117.83},
    {"city": "Newark", "latitude": 40.73, "longitude": -74.17},
    {"city": "Durham", "latitude": 35.99, "longitude": -78.9},
    {"city": "Chula Vista", "latitude": 32.64, "longitude": -117.08},
    {"city": "Toledo", "latitude": 41.65, "longitude": -83.54},
    {"city": "Fort Wayne", "latitude": 41.08, "longitude": -85.14},
    {"city": "St. Petersburg", "latitude": 27.77, "longitude": -82.64},
    {"city": "Laredo", "latitude": 27.53, "longitude": -99.49},
    {"city": "Jersey City", "latitude": 40.71, "longitude": -74.07},
    {"city": "Chandler", "latitude": 33.31, "longitude": -111.84},
    {"city": "Madison", "latitude": 43.07, "longitude": -89.4},
    {"city": "Lubbock", "latitude": 33.58, "longitude": -101.88},
    {"city": "Scottsdale", "latitude": 33.49, "longitude": -111.92},
    {"city": "Reno", "latitude": 39.53, "longitude": -119.81},
    {"city": "Buffalo", "latitude": 42.89, "longitude": -78.88},
    {"city": "Gilbert", "latitude": 33.35, "longitude": -111.79},
    {"city": "Glendale", "latitude": 34.14, "longitude": -118.25},
    {"city": "North Las Vegas", "latitude": 36.2, "longitude": -115.12},
    {"city": "Winston-Salem", "latitude": 36.1, "longitude": -80.26},
    {"city": "Chesapeake", "latitude": 36.77, "longitude": -76.29},
    {"city": "Norfolk", "latitude": 36.85, "longitude": -76.29},
    {"city": "Fremont", "latitude": 37.55, "longitude": -121.98},
    {"city": "Garland", "latitude": 32.91, "longitude": -96.64},
    {"city": "Irving", "latitude": 32.81, "longitude": -96.95},
    {"city": "Hialeah", "latitude": 25.86, "longitude": -80.3},
    {"city": "Richmond", "latitude": 37.54, "longitude": -77.43},
    {"city": "Boise", "latitude": 43.62, "longitude": -116.2},
    {"city": "Spokane", "latitude": 47.66, "longitude": -117.43},
    {"city": "Baton Rouge", "latitude": 30.45, "longitude": -91.15},
    {"city": "Tacoma", "latitude": 47.25, "longitude": -122.44}
]


    url = config.OPENMETEO_API
    all_data = pd.DataFrame()

    for city in cities:
        params = {
            "latitude": city['latitude'],
            "longitude": city['longitude'],
            "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
                       "precipitation_probability", "precipitation", "rain", "showers", "snowfall",
                       "cloud_cover", "visibility", "wind_speed_10m", "wind_direction_10m",
                       "uv_index", "uv_index_clear_sky", "is_day"]
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        hourly = response.Hourly()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }

        # Populate the DataFrame with weather data
        hourly_data.update({
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
            "dew_point_2m": hourly.Variables(2).ValuesAsNumpy(),
            "apparent_temperature": hourly.Variables(3).ValuesAsNumpy(),
            "precipitation_probability": hourly.Variables(4).ValuesAsNumpy(),
            "precipitation": hourly.Variables(5).ValuesAsNumpy(),
            "rain": hourly.Variables(6).ValuesAsNumpy(),
            "showers": hourly.Variables(7).ValuesAsNumpy(),
            "snowfall": hourly.Variables(8).ValuesAsNumpy(),
            "cloud_cover": hourly.Variables(9).ValuesAsNumpy(),
            "visibility": hourly.Variables(10).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(11).ValuesAsNumpy(),
            "wind_direction_10m": hourly.Variables(12).ValuesAsNumpy(),
            "uv_index": hourly.Variables(13).ValuesAsNumpy(),
            "uv_index_clear_sky": hourly.Variables(14).ValuesAsNumpy(),
            "is_day": hourly.Variables(15).ValuesAsNumpy()
        })

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        hourly_dataframe["location"] = city['city']
        hourly_dataframe["latitude"] = city['latitude']
        hourly_dataframe["longitude"] = city['longitude']
        hourly_dataframe["key"] = hourly_dataframe['location'] + ' ' + hourly_dataframe['date'].astype(str)
        all_data = pd.concat([all_data, hourly_dataframe], ignore_index=True)

    return all_data

def get_date_range(fetch_date):
    start_date = datetime.strptime(fetch_date, '%Y-%m-%d').date()
    end_date = start_date + timedelta(days=6)
    return start_date, end_date

def get_file_path(fetch_date):
    start_date, _ = get_date_range(fetch_date)
    filename = "openmeteo_{}_to_{}.csv".format(start_date, start_date + timedelta(days=6))
    return os.path.join(config.CSV_FILE_DIR, filename)

def get_new_data(df, fetch_date):
    start_date, end_date = get_date_range(fetch_date)
    df = df.sort_values(by=['date'], ascending=True)
    data_to_append = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    return data_to_append

def save_new_data_to_csv(data_to_append, fetch_date):
    filename = get_file_path(fetch_date)
    if not data_to_append.empty:
        data_to_append.to_csv(filename, encoding='utf-8', index=False)

def main(fetch_date):
    df = ingest_weather_data()
    data_to_append = get_new_data(df, fetch_date)
    save_new_data_to_csv(data_to_append, fetch_date)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, type=str)
    args = parser.parse_args()
    main(args.date)
