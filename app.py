from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "d22b1b5da494100b198e96bc857307e1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = ""   # define city first (for GET request)

    if request.method == "POST":
        city = request.form.get("city").title()

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if str(data.get("cod")) == "200":
            weather_data = {
                "city": city.title(),
                "temperature": round(data["main"]["temp"]),
                "description": data["weather"][0]["main"].title(),
                "humidity": data["main"]["humidity"],
                "wind": round(data["wind"]["speed"] * 3.6, 2),
            }
        else:
            weather_data = {"error": "City not found"}

    return render_template("index.html", weather=weather_data, city=city)

if __name__ == "__main__":
    app.run(debug=True)
