import ApiCall
import SQLExecute
import JsonParse
from datetime import datetime


def indexFix(array_elements):
    for index in range(len(array_elements)):
        if array_elements[index] == 'humidity':
            array_elements[index] = 'temp'
        elif array_elements[index] == 'temp':
            array_elements[index] = 'humidity'
    return array_elements


class Forecast:
    @staticmethod
    def ForecastWeather(value):
        sql = SQLExecute.SqlFunctions()
        conn = sql.conn
        attr = []
        attr_type = []
        insert_to = []
        api_names = ['Dark Sky', 'Weather Bit', 'Open Weather']
        dates = []
        print('Collect Json Paths and Attribute Types from the database:')
        for x in api_names:
            attr_class = SQLExecute.SelectApiAttributes(x, conn)
            attr.append(attr_class.selectPath())
            attr_type.append(attr_class.selectAttrType())
        print('OK')
        print('Api:')
        print('Dark Sky Weather')
        dark_json = JsonParse.DarkSkycollect(ApiCall.DarkSky(value).Forecast(), attr[0])
        insert_to.append(dark_json.ForecastDataCollector)
        dates.append(dark_json.ForecastDate())
        print('Weather Bit')
        wb_json = JsonParse.WeatherBitcollect(ApiCall.WeatherBit(value).Forecast(), attr[1])
        insert_to.append(wb_json.ForecastDataCollector())
        dates.append(wb_json.ForecastDate())
        print('Open Weather')
        open_json = JsonParse.OpenWcollect(ApiCall.OpenWeather(value).Forecast(), attr[2])
        insert_to.append(open_json.ForecastDataCollector())
        dates.append(open_json.ForecastDate())
        attr[2] = indexFix(attr[2])

        print('Insert: ')
        for index in range(len(api_names)):
            print('Currently inserting: ' + api_names[index])
            for x in range(len(insert_to[index])):
                insert_weather_data = SQLExecute.SQLInsertData(attr[index], insert_to[index][x], attr_type[index],
                                                               value,
                                                               api_names[index],
                                                               datetime.fromtimestamp(dates[index][x]),
                                                               conn)
                insert_weather_data.InsertValues()
        print('OK')
