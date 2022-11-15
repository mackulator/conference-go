import json
import requests

from .keys import OPEN_WEATHER_API_KEY, PEXELS_API_KEY


def get_weather(city, state):
    params = {
        "q": f"{city}, {state}, 'US'",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = "https://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)

    content = json.loads(response.content)

    try:
        lat = content[0]["lat"]
        lon = content[0]["lon"]
    except (KeyError, IndexError):
        return None

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)

    content = json.loads(response.content)

    print(content)
    try:
        return {
            "description": content["weather"][0]["description"],
            "temp": content["main"]["temp"],
        }
    except (KeyError, IndexError):
        return None


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"per_page": 1, "query": city + " " + state}
    url = "https://api.pexels.com/v1/search"  # response comes from this api
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(
        response.content
    )  # we want everything to be in 1 dictionary
    try:  # error handling code
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}
