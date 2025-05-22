import requests

API_KEY = '6d2f35e28e8d19faa9861db0071344d0'  #Replace with your current openweathermap API_KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity']
        }
    else:
        print(f"Error: Failed to fetch weather for {city} (status code: {response.status_code})")
        return None
