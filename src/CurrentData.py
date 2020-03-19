# Most nincs használatban

import datetime

import JsonParse
import SQLExecute
import WeatherAPI


class CurrentData:
    @staticmethod
    def CurrentData(value):
        # CON + SELECT
        sql = SQLExecute.SQLConnection()
        conn = sql.__conn
        attr = []
        attr_type = []
        to_insert = []
        api_names = ['Dark Sky', 'Weather Bit', 'Open Weather', 'Accu Weather']
        print("Collect Json Paths and Attribute Types from the database:")
        for x in api_names:
            attr_class = SQLExecute.APIAttributes(x, conn)
            attr.append(attr_class.get_path())
            attr_type.append(attr_class.get_attr_type())

        # JSON
        print('OK')
        print('Api + JSON:')
        print('Dark Sky Weather')
        dark_json = JsonParse.DarkSkycollect(WeatherAPI.DarkSky(value).current_cast(), attr[0])
        to_insert.append(dark_json.CurrentDataCollector())
        print('Weather Bit')
        wb_json = JsonParse.WeatherBitcollect(WeatherAPI.WeatherBit(value).current_cast(), attr[1])
        to_insert.append(wb_json.CurrentDataCollector())
        print('Open Weather')
        open_json = JsonParse.OpenWeathercollect(WeatherAPI.OpenWeather(value).current_cast(), attr[2])
        to_insert.append(open_json.CurrentDataCollector())
        attr[2] = JsonParse.indexFix(attr[2])
        print('Accu Weather')
        accu_json = JsonParse.AccuWeathercollect(WeatherAPI.AccuWeather(value).current_cast(), attr[3])
        to_insert.append(accu_json.CurrentDataCollector())

        print('Insert: ')
        for index in range(len(api_names)):
            print('Currently inserting: ' + api_names[index])
            insert_weather_data = SQLExecute.SQLInsertData(attr[index], to_insert[index], attr_type[index], value,
                                                           api_names[index], datetime.datetime.now(),
                                                           conn)
            insert_weather_data.InsertValues()
