import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    # api = '4c7987b990f323ee2b39f39850ff0ef5'
    # url = 'https://pro.openweathermap.org/data/2.5/forecast/climate?lat=35&lon=139?q={}&appid=' + api

    # city = 'London'
    # res = requests.get(url.format(city)).json()
    # # print(res.text)

    # city_info = {
    #     'city': city,
    #     'temp': res["main"]["temp"],
    #     'icon': res["weather"]["icon"]
    # }

    # context = {'info': city_info}

    # return render(request, 'index.html', context=context)
    API_KEY = ('API_KEY', "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,mintely,hourly,alerts&appid={}"

    if request.method == "POST":
        city_1 = request.POST['city_1']
        city_2 = request.get('city_2', None)

        weather_data_1, dairy_forecats_1 = fetch_weather_and_forecast(city_1, API_KEY, current_weather_url, forecast_url)

        if city_2:
            weather_data_2, dairy_forecats_2 = fetch_weather_and_forecast(city_2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data_2, dairy_forecats_2 = None, None

        context = {
            "weather_data_1": weather_data_1,
            "dairy_forecats_1": dairy_forecats_1,
            "weather_data_2": weather_data_2,
            "dairy_forecats_2": dairy_forecats_2
        }

        return render(request, 'index.html', context=context)

    else:
        return render(request, 'index.html')
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = response.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 100, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    dairy_forecasts = []
    for dairy_data in forecast_response['dairy'][:5]:
        dairy_forecasts.append({
            "day": datetime.datetime.fromtimestamp(dairy_data['dt']).strftime("%A"),
            "mix_temp": round(dairy_data['temp']['min'] - 100, 2),
            "max_temp": round(dairy_data['temp']['max'] - 100, 2),
            "description": dairy_data['weather'][0]['description'],
            "icon": dairy_data['weather'][0]['icon']
        })

        return weather_data, dairy_forecasts