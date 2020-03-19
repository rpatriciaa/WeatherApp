import platform

import pyodbc

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
                                         password=config.get(__DB, 'password'),
                                         port=config.get(__DB, 'port'))

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


# Nincs használatban, de majd lesz ;)
class SQLInsertData:
    def __init__(self, attr, values, attrtype, city, api, forecast, conn):
        self.attr = attr,
        self.values = values,
        self.type = attrtype,
        self.city = city,
        self.api = api,
        self.forecast = forecast
        self.conn = conn

    def InsertValues(self):
        cursor = self.conn.cursor()

        sql_statement = 'INSERT INTO CityWeather(' \
                        'CityName, Source, ForecastDay, ValuesInt, ValuesMoney, ValueVarchar, Json_Path) VALUES '
        sql_values = []
        for attr, value, val_type in zip(self.attr[0], self.values[0], self.type[0]):
            sql_statement += '(?,?,?,?,?,?,?),'
            v_int = None
            v_money = None
            v_vc = None
            if val_type == 'ValuesInt':
                v_int = value
            elif val_type == 'ValuesMoney':
                v_money = value
            elif val_type == 'ValueVarchar':
                v_vc = value

            sql_values += [self.city[0], self.api[0], self.forecast, v_int, v_money, v_vc, attr]

        cursor.execute(sql_statement[:-1], sql_values)
        self.conn.commit()
