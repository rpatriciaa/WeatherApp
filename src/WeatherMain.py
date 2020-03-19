import datetime

import WeatherAPI
from JsonParse import DataCollector
from SQLExecute import Cities, APIs


def main():
    print(datetime.datetime.now())
    cities = Cities()
    apis = APIs()
    for city in cities.cities:
        # try:
        print('City: ' + city)

        for api in apis.APIs:
            api_name = api['api']['Name']
            print('\t\t' + api_name, end='\t')

            class_name = api['api']['APIName']

            api_class = getattr(WeatherAPI, class_name)
            __api = api_class(city, api)

            print('current...', end='\t')
            current_cast_json = __api.current_cast()
            print('forecast...', end='\t')
            forecast_json = __api.forecast()

            data = DataCollector(current_cast_json, forecast_json, api)
            current_cast_data = data.current_cast_data_collector()
            forecast_data = data.forecast_data_collector()

            print('Done')

    # except TypeError:
    #     continue


if __name__ == '__main__':
    main()
