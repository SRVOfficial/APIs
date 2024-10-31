import requests

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Constants
API_KEY = os.getenv("WEATHER_API")
BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_geo_data(api_key):
    """Fetches latitude and longitude for a given city, state, and country."""

    city_name = input("City: ")
    state_code = input("State code: ")
    country_code = input("Country code: ")

    if not city_name or not country_code:
        raise ValueError("City name and country code are required.")

    geo_url = f"{BASE_GEO_URL}?q={city_name},{state_code},{country_code}&appid={api_key}"

    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        data = response.json()

        if data:
            data = data[0]
            latitude = data["lat"]
            longitude = data["lon"]
            return latitude, longitude
        else:
            raise Exception("Error: Could not fetch latitude and longitude.")

    except requests.exceptions.RequestException as e:
        raise Exception("Network error while fetching geo data.") from e


def get_weather_info(lat, lon, api_key):
    """Fetches weather information for the given latitude and longitude."""
    url = f"{BASE_WEATHER_URL}?lat={lat}&lon={lon}&appid={api_key}"
    result = {}

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            # Extract weather description
            if "weather" in data:
                result["description"] = data["weather"][0]["description"]

            # Extract main weather data
            if "main" in data:
                main_data = data["main"]
                result["temp"] = f"{main_data['temp'] - 273.15:.2f} °C"
                result["pressure"] = f"{main_data['pressure']} hPa"
                result["humidity"] = f"{main_data['humidity']}%"
                result["sea_level"] = f"{main_data.get('sea_level', 'N/A')} hPa"
                result["grnd_level"] = f"{main_data.get('grnd_level', 'N/A')} hPa"

            # Extract wind data
            if "wind" in data:
                wind_data = data["wind"]
                result["speed"] = f"{wind_data['speed'] * 2.237:.2f} miles/hour"
                result["deg"] = f"{wind_data['deg']} degrees"
                result["gust"] = f"{wind_data.get('gust', 0) * 2.237:.2f} miles/hour" if "gust" in wind_data else "N/A"

            # Extract precipitation data
            if "rain" in data:
                rain_data = data["rain"]
                result["precipitation"] = f"{rain_data.get('1h', 0)} mm/hr"

            return result
        else:
            raise Exception("Error fetching weather information.")

    except requests.exceptions.RequestException as e:
        raise Exception("Network error while fetching weather data.") from e


def main():
    try:
        latitude, longitude = get_geo_data(API_KEY)
        print(f"Latitude: {latitude} \nLongitude: {longitude}")

        weather_data = get_weather_info(latitude, longitude, API_KEY)

        print("\nWeather Information:")
        for key, value in weather_data.items():
            print(f"{key}: {value}")

    except ValueError as e:
        print("Input Error:", e)
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
