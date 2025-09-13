import importlib

data = importlib.import_module('02_data')

data = data.data
<<<<<<< HEAD
weather_data = data.weather_data

if __name__ == "__main__":
    file_path = '01_Input/Global-Oil-and-Gas-Extraction-Tracker-Feb-2025.xlsx'
    data(file_path)
    weather_data(file_path)
=======

if __name__ == "__main__":
    file_path = '01_Input/Global-Oil-and-Gas-Extraction-Tracker-Feb-2025.xlsx'
    data(file_path)
>>>>>>> df364a0 (test)
