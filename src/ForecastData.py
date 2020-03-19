# Most nincs használatban

import SQLExecute
import WeatherAPI


class Forecast:
    @staticmethod
    def forecastweather(city):
        # sql = SQLExecute.SQLConnection()
        # conn = sql.connection()
        # attr = []
        # attr_type = []
        # insert_to = []
        apis = SQLExecute.APIs()
        # dates = []
        # print('Api + JSON:')
        for api in apis.APIs:
            api_name = api['api']['Name']
            print(api_name)

            class_name = api['api']['APIName']
            api_class = getattr(WeatherAPI, class_name)
            api = api_class(city, api)
            print(city, api.location_key())

            # current_cast_json = api.current_cast()
            # forecast_json = api.forecast()

            # data = JsonParse.Test(current_cast_json, forecast_json, api)
            # current_cast_data = data.currentcast_data_collector()
            # forecast_data = data.forecast_data_collector()
            print('Ok')

        # print('Dark Sky Weather')
        # dark_json = JsonParse.DarkSkycollect(WeatherAPI.DarkSky(value).forecast(), attr[0])
        # insert_to.append(dark_json.ForecastDataCollector)
        # dates.append(dark_json.ForecastDate())
        # print('Weather Bit')
        # wb_json = JsonParse.WeatherBitcollect(WeatherAPI.WeatherBit(value).forecast(), attr[1])
        # insert_to.append(wb_json.ForecastDataCollector())
        # dates.append(wb_json.ForecastDate())
        # print('Open Weather')
        # open_json = JsonParse.OpenWeathercollect(WeatherAPI.OpenWeather(value).forecast(), attr[2])
        # insert_to.append(open_json.ForecastDataCollector())
        # dates.append(open_json.ForecastDate())
        # attr[2] = JsonParse.indexFix(attr[2])
        #
        # print('Insert: ')
        # for index in range(len(api_names)):
        #     print('Currently inserting: ' + api_names[index])
        #     for api in range(len(insert_to[index])):
        #         insert_weather_data = SQLExecute.SQLInsertData(attr[index], insert_to[index][api], attr_type[index],
        #                                                        value,
        #                                                        api_names[index],
        #                                                        datetime.fromtimestamp(dates[index][api]),
        #                                                        conn)
        #         insert_weather_data.InsertValues()
        # print('OK')
