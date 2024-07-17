import pprint

import requests

weather_codes = {
    '0': 'Солнечно',
    '1': 'Преимущественно ясно',
    '2': 'Переменная облачность',
    '3': 'Пасмурно',
    '45': 'Туман',
    '48': 'Оседающая изморозь',
    '51': 'Морось: слабая',
    '53': 'Морось: умеренная',
    '55': 'Морось: интенсивная',
    '56': 'Замерзающая морось: слабая',
    '57': 'Замерзающая морось: сильная',
    '61': 'Дождь: слабый',
    '63': 'Дождь: умеренный',
    '65': 'Дождь: сильный',
    '66': 'Небольшой град',
    '67': 'Сильный град',
    '71': 'Снегопад: слабый',
    '73': 'Снегопад: умеренный',
    '75': 'Снегопад: сильный',
    '77': 'Снежные зерна',
    '80': 'Слабый ливень',
    '81': 'Умеренный ливень',
    '82': 'Сильный ливень',
    '85': 'Снежные ливни: слабые',
    '86': 'Снежные ливни: сильные',
    '95': 'Гроза: слабая или умеренная',
    '96': 'Гроза с небольшим градом',
    '99': 'Гроза с сильным градом'
}


def get_coordinates(city):
	nominatim_url = f'https://nominatim.openstreetmap.org/search?q={city}&format=json'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36'
	}
	response = requests.get(nominatim_url, headers=headers)
	if response.status_code == 200:
		data = response.json()
		if data:
			return data[0]['lat'], data[0]['lon']


def get_weather(city, time):
	coordinates = get_coordinates(city)

	api_url = f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=weather_code,temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=Europe%2FMoscow'
	response = requests.get(api_url)

	if response.status_code == 200:
		data = response.json()
		return convert_data(data, time)

def convert_data(weather, time):
	weather_data = []
	if time == 'today':
		hours_start = 0
		hours_end = 24
		_split = 1
	elif time == 'yesterday':
		hours_start = 24
		hours_end = 48
		_split = 1
	elif time == '3days':
		hours_start = 13
		hours_end = 72
		_split = 24
	elif time == 'week':
		hours_start = 13
		hours_end = len(weather['hourly']['time'])
		_split = 24

	for i in range(hours_start, hours_end, _split):
		weather_code = weather['hourly']['weather_code'][i]
		weather_description = weather_codes[str(weather_code)]



		data_dict = {
			'time': weather['hourly']['time'][i],  # Время
			'temperature': weather['hourly']['apparent_temperature'][i],  # Температура по ощущениям
			'precipitation': weather['hourly']['precipitation'][i],  # Осадки мм
			'precipitation_probability': weather['hourly']['precipitation_probability'][i],  # Вероятность осадков %
			'pressure_msl': weather['hourly']['pressure_msl'][i],  # Давление гПа
			'temperature_fact': weather['hourly']['temperature_2m'][i],  # Температура фактическая
			'wind_direction': weather['hourly']['wind_direction_10m'][i],  # Направление ветра в градусах
			'wind_speed': weather['hourly']['wind_speed_10m'][i],  # Скорость ветра'
			'relative_humidity': weather['hourly']['relative_humidity_2m'][i],   #Влажность  %
			'weather': weather_description    # Погода (солнечно, ливень и тд)
		}
		weather_data.append(data_dict)
	return weather_data