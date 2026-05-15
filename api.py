import requests
import json
from deep_translator import GoogleTranslator


def get(sity):
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'

    geocoder_request = (
        f'https://geocode-maps.yandex.ru/v1/'
        f'?apikey={api_key}'
        f'&geocode={sity}'
        f'&format=json'
    )

    response = requests.get(geocoder_request)

    if response:
        data = response.json()

        point = (
            data['response']['GeoObjectCollection']
            ['featureMember'][0]['GeoObject']['Point']['pos']
        )

        lon, lat = point.split()

    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)

    print("Http статус:", response.status_code, "(", response.reason, ")")

    API_KEY = "fa0f11a5-fd86-48c2-b07f-ef6e45a933a8"

    headers = {
        "X-Yandex-Weather-Key": API_KEY
    }

    query = f"""{{
        weatherByPoint(request: {{ lat: {lat}, lon: {lon} }}) {{
            now {{
                temperature
                humidity
                pressure
                windSpeed
                cloudiness
            }}
        }}
    }}"""

    response = requests.post(
        'https://api.weather.yandex.ru/graphql/query',
        headers=headers,
        json={'query': query}
    )

    if response.status_code == 200:
        data = response.json()

        temp = data['data']['weatherByPoint']['now']['temperature']

        humidity = (
            f"{data['data']['weatherByPoint']['now']['humidity']}%"
        )

        cloudiness = data['data']['weatherByPoint']['now']['cloudiness']

        # перевод (не очень получился)
        cloudiness = GoogleTranslator(
            source='auto',
            target='ru'
        ).translate(cloudiness)

    else:
        print(response.text)

    return sity, lat, lon, temp, humidity, cloudiness