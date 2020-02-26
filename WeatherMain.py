import sys
from CurrentData import CurrentData
from ForecastData import Forecast
import schedule
import time
import datetime


def main():
    print(datetime.datetime.now())
    for x in sys.argv[1::]:
        try:
            print('City: ' + x)
            print('Forecast: ')
            Forecast.ForecastWeather(x)
            print('Finished.')

            print('Current:')
            CurrentData.CurrentData(x)
            print('Finished.')
        except TypeError:
            continue


if __name__ == '__main__':
    main()