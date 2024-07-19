import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    api = '4c7987b990f323ee2b39f39850ff0ef5'
    url = 'https://pro.openweathermap.org/data/2.5/forecast/climate?lat=35&lon=139?q={}&appid=' + api

    city = 'London'
    res = requests.get(url.format(city))
    print(res.text)

    return render(request, 'index.html')