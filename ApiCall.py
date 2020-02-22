from abc import ABC, abstractmethod

import requests
from geopy.geocoders import Nominatim


class ApiCall(ABC):
    def __init__(self, location):
        self.location = location
        super().__init__()

    @abstractmethod
    def CurrentCall(self):
        pass

    @abstractmethod
    def Forecast(self):
        pass


class AccuWeather(ApiCall):
    def LocationKey(self):
        response = requests.get("http://dataservice.accuweather.com/locations/v1/cities/search?apikey"
                                "=G6XBgWa9eLvzcIIRsJj6abhi4OsEXz0k&q=" + self.location + ",HU&language=en-us")
        if response.status_code == 200:
            key_search = response.json()
            locationkey = key_search[0]["Key"]
            return locationkey
        else:
            return "Error"

    def CurrentCall(self):
        locationkey = self.LocationKey()
        if locationkey != "Error":
            response = requests.get("http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"
                                    + locationkey + "?apikey=%09G6XBgWa9eLvzcIIRsJj6abhi4OsEXz0k&language=en-us"
                                                    "&details=true&metric=true")
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return status_code
        else:
            return "Could not reach location through AccuWeather"

    def Forecast(self):
        locationkey = self.LocationKey()
        if locationkey != "Error":
            response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
                                    + locationkey + "?apikey=%09G6XBgWa9eLvzcIIRsJj6abhi4OsEXz0k&language=en-us"
                                                    "&details=true&metric=true")
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return status_code
        else:
            return "Could not reach location through AccuWeather"


class WeatherBit(ApiCall):
    def CurrentCall(self):
        response = requests.get(
            "https://api.weatherbit.io/v2.0/current?city=" + self.location +
            "&country=HU"
            "&tz=local&key=5bfdc7a7a51841cc9ddb4f35462ae665&units=metric")
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            return status_code

    def Forecast(self):
        response = requests.get(
            "https://api.weatherbit.io/v2.0/forecast/daily?city=" + self.location +
            "&country=HU"
            "&tz=local&key=5bfdc7a7a51841cc9ddb4f35462ae665&units=metric&days=6")
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            return status_code


class DarkSky(ApiCall):
    def CurrentCall(self):
        geolocator = Nominatim(user_agent="WeatherApp")
        location = geolocator.geocode(self.location)
        lat = location.latitude
        long = location.longitude
        loc_string = str(lat) + "," + str(long)
        response = requests.get(
            "https://api.darksky.net/forecast/d43412fab3e9aa840c40c50ad38cc6e9/" + loc_string +
            "?&units=ca&lang=en")
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            return status_code

    def Forecast(self):
        geolocator = Nominatim(user_agent="WeatherApp")
        location = geolocator.geocode(self.location)
        lat = location.latitude
        long = location.longitude
        loc_string = str(lat) + "," + str(long)
        response = requests.get(
            "https://api.darksky.net/forecast/d43412fab3e9aa840c40c50ad38cc6e9/" + loc_string +
            "?exclude=daily&extend=hourly&units=ca&lang=en")
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            return status_code


class OpenWeather(ApiCall):
    def CurrentCall(self):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q=" + self.location +
            ",hu&units=metric&appid=63f727b2e84f011a46f960fd7e1a3680&%22")
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            return status_code

    def Forecast(self):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast?q=" + self.location +
            ",hu&units=metric&appid=63f727b2e84f011a46f960fd7e1a3680&%22")
        status_code = response.status_code
        if status_code == 200:
            return response.json()["list"]
        else:
            return status_code
