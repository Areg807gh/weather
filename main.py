import requests
from flask import Flask, render_template, request
from api import get

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For',request.remote_addr).split(',')[0].strip()
    if ip == "127.0.0.1": #если localhost
        city = "Барнаул"
    else:

        data = requests.get(
            f"http://ip-api.com/json/{ip}"
        ).json()

        city = data.get("city")

    result = get(city)
    city_name, lat, lon, temp, humidity, cloudiness = result

    if temp is None:
        error_msg = f"Не удалось получить погоду для города {city_name}"
        return render_template("index.html", city=city_name, lat=lat, lon=lon,
                                      temp=None, humidity=None, cloudiness=None, error=error_msg)

    return render_template(
        "index.html",
        city=city_name,
        lat=lat,
        lon=lon,
        temp=temp,
        humidity=humidity,
        cloudiness=cloudiness,
        error=None
    )

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
