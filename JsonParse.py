from abc import ABC, abstractmethod


def indexFix(array_elements):
    for index in range(len(array_elements)):
        if array_elements[index] == 'humidity':
            array_elements[index] = 'temp'
        elif array_elements[index] == 'temp':
            array_elements[index] = 'humidity'
    return array_elements


class AbsractDataCollector(ABC):
    def __init__(self, jsonobject, attr):
        self.jsonobject = jsonobject
        self.attr = attr

    @abstractmethod
    def CurrentDataCollector(self):
        pass

    @abstractmethod
    def ForecastDataCollector(self):
        pass

    @abstractmethod
    def ForecastDate(self):
        pass


class DarkSkycollect(AbsractDataCollector):
    def __init__(self, jsonobject, attr):
        super().__init__(jsonobject, attr)
        self.data = self.jsonobject

    def CurrentDataCollector(self):
        values = []
        for x in self.attr:
            try:
                values.append(self.data["currently"][x])
            except KeyError:
                values.append('Clear')
        return values

    @property
    def ForecastDataCollector(self):
        values = []
        for i in range(0, 130):
            valuerefs = []
            for x in self.attr:
                try:
                    valuerefs.append(self.data['hourly']['data'][i][x])
                except KeyError:
                    valuerefs.append('Clear')
            values.append(valuerefs)
            valuerefs[:]
        return values

    def ForecastDate(self):
        dates = []
        for i in range(0, 130):
            dates.append(self.data['hourly']['data'][i]['time'])
        return dates


class WeatherBitcollect(AbsractDataCollector):
    def __init__(self, jsonobject, attr):
        super().__init__(jsonobject, attr)
        self.data = self.jsonobject["data"]

    def CurrentDataCollector(self):
        values = []
        for x in self.attr:
            try:
                if x == "description":
                    values.append(self.data[0]['weather'][x])
                else:
                    values.append(self.data[0][x])
            except TypeError:
                values.append(0)
        return values

    def ForecastDataCollector(self):
        values = []
        for i in range(1, 6):
            valuerefs = []
            for x in self.attr:
                try:
                    if x == "description":
                        valuerefs.append(self.data[i]['weather'][x])
                    else:
                        valuerefs.append(self.data[i][x])
                except TypeError:
                    valuerefs.append(0)
                except KeyError:
                    continue
            values.append(valuerefs)
            valuerefs[:]
        return values

    def ForecastDate(self):
        dates = []
        for i in range(1, 6):
            dates.append(self.data[i]['ts'])
        return dates


class Accucollect(AbsractDataCollector):
    def __init__(self, jsonobject, attr):
        super().__init__(jsonobject, attr)
        self.data = self.jsonobject[0]

    def CurrentDataCollector(self):
        values = []
        for x in self.attr:
            try:
                if x == 'Speed':
                    values.append(self.data['Wind'][x]['Value'])
                elif x == 'Direction':
                    values.append(self.data['Wind'][x]['Degrees'])
                else:
                    values.append(self.data[x]['Value'])
            except TypeError:
                values.append(self.data[x])
        return values

    def ForecastDataCollector(self):
        pass

    def ForecastDate(self):
        pass


class OpenWcollect(AbsractDataCollector):
    def __init__(self, jsonobject, attr):
        super().__init__(jsonobject, attr)
        self.data = self.jsonobject

    def CurrentDataCollector(self):
        values = []
        for x in self.data:
            try:
                for z in self.data.get(x):
                    for y in self.attr:
                        if z == y:
                            values.append(self.data[x][z])
            except TypeError:
                continue
        return values

    def ForecastDataCollector(self):
        values = []
        for i in range(0, 40):
            valuerefs = []
            for x in self.data[i]:
                try:
                    for z in self.data[i][x]:
                        for y in self.attr:
                            if z == y:
                                valuerefs.append(self.data[i][x][z])
                except TypeError:
                    continue
            values.append(valuerefs)
            valuerefs[:]
        return values

    def ForecastDate(self):
        dates = []
        for x in range(0, 40):
            dates.append(self.data[x]['dt'])
        return dates
