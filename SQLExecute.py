import pyodbc


def CharacterReplace(string):
    string = string.replace("Decimal", "")
    string = string.strip("(),' ")
    return string


class SqlFunctions:
    def __init__(self):
        self.conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                                   server='localhost', database='TestDatabase',
                                   trusted_connection='yes')

    def connection(self):
        conn = self.conn
        return conn

    def close(self):
        self.conn.close()


class SelectApiAttributes:
    def __init__(self, apiname, conn):
        self.ApiName = apiname,
        self.conn = conn

    def selectPath(self):
        values = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT Json_Path FROM TestDatabase..SelectAttr WHERE Source = ?', self.ApiName)
        for row in cursor:
            string = str(row)
            string = CharacterReplace(string)
            values.append(string)
        return values

    def selectAttrType(self):
        values = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT AttrType FROM TestDatabase..SelectAttr WHERE Source = ?', self.ApiName)
        for row in cursor:
            string = str(row)
            string = CharacterReplace(string)
            values.append(string)
        return values


class SQLInsertData:
    def __init__(self, attr, values, attrtype, city, api,forecast, conn):
        self.attr = attr,
        self.values = values,
        self.type = attrtype,
        self.city = city,
        self.api = api,
        self.forecast = forecast
        self.conn = conn

    def InsertValues(self):
        cursor = self.conn.cursor()

        sql_statement = 'INSERT INTO TestDatabase..CityWeather(' \
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

            sql_values += [self.city[0], self.api[0],self.forecast, v_int, v_money, v_vc, attr]

        cursor.execute(sql_statement[:-1], sql_values)
        self.conn.commit()
