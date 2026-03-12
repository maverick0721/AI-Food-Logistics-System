import random


class WeatherModel:

    def current_weather(self):

        weather = ["clear", "rain", "storm"]

        return random.choice(weather)