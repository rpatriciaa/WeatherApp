import ApiCall
import SQLExecute
import JsonParse
import datetime


class CurrentData:
    @staticmethod
    def CurrentData(value):
        # CON + SELECT
        sql = SQLExecute.SqlFunctions()
        conn = sql.conn
        attr = []
        attr_type = []
        to_insert = []
        api_names = ['Dark Sky', 'Weather Bit', 'Open Weather', 'Accu Weather']
        for x in api_names:
            attr_class = SQLExecute.SelectApiAttributes(x, conn)
            attr.append(attr_class.selectPath())
            attr_type.append(attr_class.selectAttrType())

        # JSON
        print('Dark')
        dark_json = JsonParse.DarkSkycollect(ApiCall.DarkSky(value).CurrentCall(), attr[0])
        print('WB')
        wb_json = JsonParse.WeatherBitcollect(ApiCall.WeatherBit(value).CurrentCall(), attr[1])
        print('Open')
        open_json = JsonParse.OpenWcollect(ApiCall.OpenWeather(value).CurrentCall(), attr[2])
        print('Accu')
        accu_json = JsonParse.Accucollect(ApiCall.AccuWeather(value).CurrentCall(), attr[3])

        to_insert.append(dark_json.CurrentDataCollector())
        to_insert.append(wb_json.CurrentDataCollector())
        to_insert.append(open_json.CurrentDataCollector())
        to_insert.append(accu_json.CurrentDataCollector())

        for index in range(len(api_names)):
            insert_weather_data = SQLExecute.SQLInsertData(attr[index], to_insert[index], attr_type[index], value,
                                                           api_names[index], datetime.datetime.now(),
                                                           conn)
            insert_weather_data.InsertValues()
