import json
from abc import ABC


class DataCollector(ABC):
    def __init__(self, current_cast_json, forecast_json, api):
        self.current_cast_json = current_cast_json
        self.forecast_json = forecast_json
        self.api = api
        self.attrs = api['attrs']

    def current_cast_data_collector(self):
        return self.__data_collector()

    def forecast_data_collector(self):
        return self.__data_collector(False)

    def forecast_date(self):
        print('TODO')

    @staticmethod
    def __getvalue(path, data):
        value = data
        if path != '':
            path = path.split('/')
            for p in path:
                if isinstance(value, tuple) or isinstance(value, list):
                    value = value[0]
                if p in value:
                    value = value[p]
                else:
                    value = None
                    break
        return value

    @staticmethod
    def __not_a_json(data):
        try:
            json.loads(data)
        except TypeError as err:
            return True
        except ValueError as err:
            return True
        return False

    def __data_collector(self, current=True):
        if current:
            attr = 'CC'
            data = self.current_cast_json
        else:
            attr = 'FC'
            data = self.forecast_json
        if isinstance(data, int):  # AccuWeather int-ed ad vissza, ha hiba van...
            return None
        base = self.api['api']['JSON_Path_' + attr]
        attr_name = 'JSON_Attr_' + attr
        data = self.__getvalue(base, data)
        if current:
            values = self.__get_values(attr_name, data)
        else:
            values = []
            for element in data:
                values.append(self.__get_values(attr_name, element))
        return values

    def __get_values(self, attr_name, data):
        values = [{'AttrID': attr['AttrID'], 'Value': self.__getvalue(attr[attr_name], data)}
                  for attr in self.attrs]
        return values
