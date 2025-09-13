import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
<<<<<<< HEAD
=======
import time

>>>>>>> df364a0 (test)


#       Use this script to download weather data for every location on the offshore station dataset that i will provide
#
#       Then after create a xlsx or csv file with the owner/company that owns the offshore station,
#       and to have the weather data for each offshore station, next to the stock exchange name if it tradable 
#       and the Oil Market is it on (Brent, WTI, etc)

def data(file_path):
	df =  pd.read_excel(file_path, sheet_name='Main data')
	df = df[df['Onshore/Offshore'] == 'Offshore']

	model_df = df[['Operator','Unit Name','Country/Area','Latitude', 'Longitude','Onshore/Offshore']].dropna()

	date_debut = '2024-01-01'
	date_fin = '2024-01-31'
	dates = pd.date_range(start=date_debut, end=date_fin, freq='D')
	#print(dates)

	for date in dates:
		print(f"Récupération des données météo pour le {date.strftime('%Y-%m-%d')}")
		print(date)
		date = date.strftime('%Y-%m-%d')
		print(date)
		for rows in model_df.iterrows():
			latitude = rows[1]['Latitude']
			longitude = rows[1]['Longitude']
			hourly_data = historical_weather_api(latitude, longitude, date)
			time.sleep(0.1) 
			all_hourly_data = ["temperature_2m", "relative_humidity_2m", "rain", "pressure_msl", "surface_pressure", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_100m", "wind_speed_10m", "wind_gusts_10m", "shortwave_radiation", "terrestrial_radiation"]
			for data in all_hourly_data:
				model_df[data] = hourly_data[data]


		print(model_df)



# Make sure that to use the marine API, Weather API, and other Open Meteo APIs
def historical_weather_api(latitude, longitude, date):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"start_date": date,
		"end_date": date,
		"hourly": ["temperature_2m", "relative_humidity_2m", "rain", "pressure_msl", "surface_pressure", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_100m", "wind_speed_10m", "wind_gusts_10m", "shortwave_radiation", "terrestrial_radiation"],
		"models": ["era5_land", "era5_ensemble"],
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process 1 location and 2 models
	for response in responses:
		print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation: {response.Elevation()} m asl")
		print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
		print(f"Model Nº: {response.Model()}")
		
		# Process hourly data. The order of variables needs to be the same as requested.
		hourly = response.Hourly()
		hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
		hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
		hourly_rain = hourly.Variables(2).ValuesAsNumpy()
		hourly_pressure_msl = hourly.Variables(3).ValuesAsNumpy()
		hourly_surface_pressure = hourly.Variables(4).ValuesAsNumpy()
		hourly_et0_fao_evapotranspiration = hourly.Variables(5).ValuesAsNumpy()
		hourly_vapour_pressure_deficit = hourly.Variables(6).ValuesAsNumpy()
		hourly_wind_speed_100m = hourly.Variables(7).ValuesAsNumpy()
		hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()
		hourly_wind_gusts_10m = hourly.Variables(9).ValuesAsNumpy()
		hourly_shortwave_radiation = hourly.Variables(10).ValuesAsNumpy()
		hourly_terrestrial_radiation = hourly.Variables(11).ValuesAsNumpy()

		hourly_data = {"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		)}
		
		hourly_data["temperature_2m"] = hourly_temperature_2m
		hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
		hourly_data["rain"] = hourly_rain
		hourly_data["pressure_msl"] = hourly_pressure_msl
		hourly_data["surface_pressure"] = hourly_surface_pressure
		hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
		hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
		hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
		hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
		hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
		hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
		hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation
		

		return hourly_data
		# hourly_dataframe = pd.DataFrame(data = hourly_data)
		# print("\nHourly data\n", hourly_dataframe)
		
		
>>>>>>> df364a0 (test)
