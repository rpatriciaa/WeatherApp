from abc import ABC

import requests
from geopy.geocoders import Nominatim

from SQLExecute import Locations

HTTP_OK = 200
ERROR_MSG = "Error"


class WeatherAPIBase(ABC):
    def __init__(self, location, api):
        self.location = location
        self.api = api['api']
        self.config_name = {False: 'ForeCast', True: 'CurrentCast'}
        super().__init__()

    def location_key(self):
        return self.location

    def current_cast(self):
        return self.__get_cast()

    def forecast(self):
        return self.__get_cast(False)

    @staticmethod
    def request(url):
        return requests.get(url)

    def request_and_result(self, url):
        return self.__result(self.request(url))

    @staticmethod
    def __result(response):
        if response.status_code == HTTP_OK:
            return response.json()
        else:
            return response.status_code

    def __get_cast(self, current=True):
        locationkey = self.location_key()
        if locationkey != ERROR_MSG:
            return self.request_and_result(
                self.api[self.config_name.get(current)].format(url=self.api['URL'],
                                                               apikey=self.api['APIKey'],
                                                               location=locationkey))
        else:
            return "Could not reach location through {name}".format(name=self.api['Name'])


class AccuWeather(WeatherAPIBase):

    def __init__(self, location, api):
        self.sql = Locations()
        super().__init__(location, api)

    def location_key(self):
        locationkey = self.sql.get_locationkey(self.api['Name'], self.location)
        if len(locationkey) != 0:
            return locationkey[0]
        else:
            response = self.request(self.api['Location'].format(url=self.api['URL'],
                                                                apikey=self.api['APIKey'],
                                                                location=self.location))
            if response.status_code == HTTP_OK:
                locationkey = response.json()[0]['Key']
                self.sql.set_locationkey(self.api['Name'], self.location, locationkey)
                return locationkey
            else:
                return ERROR_MSG


class DarkSky(WeatherAPIBase):
    def location_key(self):
        location = Nominatim(user_agent="WeatherApp").geocode(self.location)
        return '{lat},{long}'.format(lat=location.latitude, long=location.longitude)
