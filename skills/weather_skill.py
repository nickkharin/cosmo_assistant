import os
import requests
from googletrans import Translator


class WeatherSkill:
    def __init__(self):
        api_key = os.getenv("WEATHER_API_KEY")
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.translator = Translator()

    def get_weather(self, location):
        """
        Возвращает текущую погоду для указанного местоположения.
        """
        translated_location = self.translator.translate(location, src='ru', dest='en').text
        complete_url = f"{self.base_url}appid={self.api_key}&q={translated_location}"
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != 200:
            return f"Ошибка получения данных о погоде: {weather_data['message']}, api key: {self.api_key}."

        weather = {
            'description': weather_data['weather'][0]['description'],
            'temperature': weather_data['main']['temp'],
            'city': weather_data['name']
        }

        result = (f"Погода в городе {location}: {weather['description']}, "
                  f"температура {weather['temperature']} Kelvin.")

        return result
