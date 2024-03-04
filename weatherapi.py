import requests


# from datetime import datetime, timedelta


def get_weather(latitude, longitude):
    base_url = "https://api.weatherapi.com/v1"
    endpoint = "/forecast.json"
    query = f"{latitude}, {longitude}"
    # query = "1.288662, 103.827343"
    params = {
        "key": "08d43bd24dc34261adc155152231612",
        "q": query,
        "days": 1,
    }

    try:
        response = requests.get(base_url + endpoint, params=params)
        data = response.json()
        # print(data)
        # Extract relevant weather information
        # location = data["location"]["name"]
        # local_time = data["location"]["localtime"]

        # current_time = datetime.strptime(local_time, "%Y-%m-%d %H:%M")
        # current_temp = data["current"]["temp_c"]
        current_condition = data["current"]["condition"]["text"]

        # fore_time = current_time + timedelta(hours=2)
        # fore_temp = data["forecast"]["forecastday"][0]["hour"][2]["temp_c"]  # 2 hours from now
        fore_condition = data["forecast"]["forecastday"][0]["hour"][2]["condition"]["text"]
        fore_raining = data["forecast"]["forecastday"][0]["hour"][2]["will_it_rain"]
        # fore_rain_chance = data["forecast"]["forecastday"][0]["hour"][2]["chance_of_rain"]
        fore_precip_mm = data["forecast"]["forecastday"][0]["hour"][2]["precip_mm"]
        # print(local_time, fore_time, location)

        return current_condition, fore_condition, fore_raining, fore_precip_mm

    except Exception as e:
        print(f"Error fetching weather data: {e}")
