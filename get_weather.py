import requests

def get_coordinates(city):
	nominatim_url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
	}
	response = requests.get(nominatim_url, headers=headers)
	print(response.status_code)
	if response.status_code == 200:
		data = response.json()
		if data:
			return data[0]['lat'], data[0]['lon']


def get_weather(city):
	coordinates = get_coordinates('Москва')

	api_url = f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=Europe%2FMoscow'
	response = requests.get(api_url)

	if response.status_code == 200:
		data = response.json()
		return converted_data(data)

def converted_data(weather):
	weather_data = []
	for i in range(len(weather['hourly']['time'])):
		data_dict = {
			'time': weather['hourly']['time'][i],  # Время
			'temperature': weather['hourly']['apparent_temperature'][i],  # Температура по ощущениям
			'precipitation': weather['hourly']['precipitation'][i],  # Осадки мм
			'precipitation_probability': weather['hourly']['precipitation_probability'][i],  # Вероятность осадков %
			'pressure_msl': weather['hourly']['pressure_msl'][i],  # Давление гПа
			'temperature_fact': weather['hourly']['temperature_2m'][i],  # Температура фактическая
			'wind_direction': weather['hourly']['wind_direction_10m'][i],  # Направление ветра в градусах
			'wind_speed': weather['hourly']['wind_speed_10m'][i]  # Скорость ветра
		}
		weather_data.append(data_dict)
	return  weather_data