import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry


#       Use this script to download weather data for every location on the offshore station dataset that i will provide
#
#       Then after create a xlsx or csv file with the owner/company that owns the offshore station,
#       and to have the weather data for each offshore station, next to the stock exchange name if it tradable 
#       and the Oil Market is it on (Brent, WTI, etc)

def data(file_path):
    df =  pd.read_excel(file_path, sheet_name='Main data')
    df = df[df['Onshore/Offshore'] == 'Offshore']

    locations = df[['Operator','Unit Name','Country/Area','Latitude', 'Longitude','Onshore/Offshore']].dropna()





async def weather_data(latitude, longitude):
	openmeteo = openmeteo_requests.AsyncClient()

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
		"current": ["temperature_2m", "relative_humidity_2m"],
	}
	responses = await openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

	# Process current data. The order of variables needs to be the same as requested.
	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_relative_humidity_2m = current.Variables(1).Value()

	print(f"Current time: {current.Time()}")
	print(f"Current temperature_2m: {current_temperature_2m}")
	print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")