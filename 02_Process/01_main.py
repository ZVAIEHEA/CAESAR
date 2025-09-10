import importlib

data = importlib.import_module('02_data')

weather_data = data.weather_data

if __name__ == "__main__":
    weather_data()