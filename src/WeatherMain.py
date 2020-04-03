import datetime
import WeatherAPI
from JsonParse import DataCollector
from SQLExecute import Cities, APIs, SQLInsertData, SQLConnection


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

            current_cast_json = __api.current_cast()
            forecast_json = __api.forecast()

            data = DataCollector(current_cast_json, forecast_json, api)
            forecast_date = data.forecast_data_time()
            current_cast_data = data.current_cast_data_collector()
            forecast_data = data.forecast_data_collector()

            print('current...', end='\t')
            SQLInsertData(current_cast_data, city, api_name, '').InsertData()
            print('Done')
            print('forecast...', end='\t')
            SQLInsertData(forecast_data, city, api_name, forecast_date).InsertData(False)
            print('Done')

    # except TypeError:
    #     continue


if __name__ == '__main__':
    main()
