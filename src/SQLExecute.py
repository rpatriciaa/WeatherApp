import platform
import json
import time
import pyodbc
from datetime import datetime
from Config import config


class SQLConnection:
    def __init__(self):
        __DB = 'Database'
        __drivers = {
            'Darwin': '/usr/local/lib/libtdsodbc.so',
            'Linux': '/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.4.so.1.1',
            # nem tudom, hogy linux alatt jo-e ez driver
            'Windows': '{SQL Server Native Client 11.0}'
        }
        __DRIVER = __drivers.get(platform.system())
        __SERVER = config.get(__DB, 'server')
        __DATABASE = config.get(__DB, 'database')
        if __SERVER == 'localhost':
            self.__conn = pyodbc.connect('',
                                         driver=__DRIVER,
                                         server=__SERVER,
                                         database=__DATABASE,
                                         trusted_connection='yes')
        else:
            self.__conn = pyodbc.connect('',
                                         driver=__DRIVER,
                                         server=__SERVER,
                                         database=__DATABASE,
                                         user=config.get(__DB, 'user'),
                                         password=config.get(__DB, 'password'))

    def connection(self):
        return self.__conn

    def close(self):
        self.__conn.close()

    def get_cursor(self):
        return self.__conn.cursor()

    def __get_data(self, script):
        data = []
        cursor = self.get_cursor()
        cursor.execute(script)
        if len(cursor.description) != 1:
            cols = [i[0] for i in cursor.description]
            attr_range = range(len(cols))
            for row in cursor:
                r = []
                for i in attr_range:
                    r.append(row[i])
                data.append(dict(zip(cols, r)))
        else:
            for row in cursor:
                data.append(row[0])
        return data

    @staticmethod
    def __attr(args):
        if isinstance(args, list) or isinstance(args, tuple):
            attrs = ', '.join(['[{}]'.format(a) for a in args])
        else:
            attrs = '[{}]'.format(str(args))
        return attrs.replace('[*]', '*')

    def get_data(self, table, *args):
        return self.__get_data('SELECT {attrs} FROM {table}'.format(attrs=self.__attr(args),
                                                                    table=self.__attr(table)))

    def get_filtered_data(self, table, where, *args):
        return self.__get_data(
            'SELECT {attrs} FROM {table} WHERE {filter}'.format(attrs=self.__attr(args),
                                                                table=self.__attr(table),
                                                                filter=where))


class Cities:
    def __init__(self):
        connection = SQLConnection()
        self.cities = connection.get_data('vCity', 'CityName')


class Locations:
    def __init__(self):
        self.connection = SQLConnection()

    def get_locationkey(self, api, city):
        return self.connection.get_filtered_data('vLocation',
                                                 '[AName] = \'{api}\' AND [CName] = \'{city}\''.format(api=api,
                                                                                                       city=city),
                                                 'LocationKey')

    def set_locationkey(self, api, city, locationkey):
        cursor = self.connection.get_cursor()
        cursor.execute('INSERT INTO [vLocation] ([AName], [CName], [LocationKey]) VALUES (?, ?, ?)',
                       [api, city, locationkey])
        cursor.commit()


class APIs:
    def __init__(self):
        connection = SQLConnection()
        self.APIs = []
        for data in connection.get_data('vAPI', '*'):
            d = connection.get_filtered_data('vSelectAttr',
                                             '[APIID] = {}'.format(data['APIID']),
                                             '*')
            self.APIs.append(dict(api=data, attrs=d))


class APIAttributes:
    def __init__(self, apiname, sqlconnection):
        self.ApiName = apiname,
        self.SqlConnection = sqlconnection
        self.data = sqlconnection.get_data('vSelectAttr', 'Json_Path_CC', 'Json_Path_FC', 'AttrType')


class SQLInsertData:

    def __init__(self, data, city, api, forecast):
        self.data = data
        self.city = city,
        self.api = api,
        self.forecast = forecast
        self.conn = SQLConnection().connection()
        self.cursor = SQLConnection().get_cursor()

    @staticmethod
    def set_attr_value(data, key):
        value = []
        if data is not None:
            json_data = json.loads(json.dumps(data))
            for i in json_data:
                value.append(i[key])
            return value
        else:
            return None

    @staticmethod
    def attr_type(attr):
        return SQLConnection().get_filtered_data('Attribute',
                                                 '[AttrID] = \'{attr}\''.format(attr=attr),
                                                 'AttrType')

    def insert_execute(self, attr_id, values, forecast):
        cursor = self.cursor
        sql_statement = 'INSERT INTO vCityWeather(' \
                             'ForecastDay, CityName, Name, ValuesInt, ValuesMoney, ValueVarchar, AttrID ) VALUES '
        sql_values = []
        if attr_id is not None:
            for attr, value in zip(attr_id, values):
                val_type = self.attr_type(attr)
                val_type = val_type[0]

                v_int = None
                v_money = None
                v_vc = None

                if val_type == 'ValuesInt':
                    v_int = value
                elif val_type == 'ValuesMoney':
                    v_money = value
                elif val_type == 'ValueVarchar':
                    v_vc = value

                sql_statement += '(?,?,?,?,?,?,?),'
                sql_values += [forecast, self.city[0], self.api[0], v_int, v_money, v_vc, attr]
            cursor.execute(sql_statement[:-1],sql_values)
            return self.conn.commit()
        else:
            return None

    def InsertData(self, current=True):
        if current:
            attr_id = self.set_attr_value(self.data, 'AttrID')
            values = self.set_attr_value(self.data, 'Value')
            forecast = datetime.now()
            self.insert_execute(attr_id, values, forecast)

        else:
            if self.data is not None:
                for i in range(len(self.data)):
                    if i <= 120:
                        attr_id = self.set_attr_value(self.data[i], 'AttrID')
                        values = self.set_attr_value(self.data[i], 'Value')
                        forecast = self.forecast[i]
                        self.insert_execute(attr_id, values, forecast)
                    else:
                        break

