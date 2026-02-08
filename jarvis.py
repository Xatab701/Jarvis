import pyttsx3
import SpeechRecognition as sr
import datetime
import requests
import json
import os

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.commands = {
            "время": self.get_time,
            "дата": self.get_date,
            "погода": self.get_weather,
            "информация о системе": self.get_system_info,
            "файловые операции": self.file_operations,
            "интернет команды": self.internet_commands,
            "напоминания": self.reminders,
            "таймеры": self.timers,
            "будильники": self.alarms,
            "ChatGPT": self.chatgpt_integration
        }

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio, language='ru-RU')

    def get_time(self):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.speak(f'Текущее время: {current_time}') 

    def get_date(self):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.speak(f'Сегодня: {current_date}') 

    def get_weather(self):
        response = requests.get('http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=YOUR_LOCATION&lang=ru')
        weather = response.json()
        self.speak(f"Погода в {weather['location']['name']}: {weather['current']['temp_c']} градусов")

    def get_system_info(self):
        import platform
        os_info = platform.uname()
        self.speak(f'Система {os_info.system}, Имя {os_info.node}, Версия {os_info.release}, Архитектура {os_info.machine}')

    def file_operations(self):
        self.speak('Какую файловую операцию вы хотите выполнить?')
        #Implement file operations logic

    def internet_commands(self):
        self.speak('Какую интернет команду вы хотите выполнить?')
        #Implement internet commands logic

    def reminders(self):
        self.speak('Напоминания скоро будут доступны.')

    def timers(self):
        self.speak('Таймеры скоро будут доступны.')

    def alarms(self):
        self.speak('Будильники скоро будут доступны.')

    def chatgpt_integration(self):
        self.speak('Интеграция ChatGPT скоро будет доступна.')

    def run(self):
        self.speak('Здравствуйте! Я ваш голосовой помощник.')
        while True:
            command = self.listen()
            if command in self.commands:
                self.commands[command]()
            else:
                self.speak('Извините, я не понимаю команду.')

if __name__ == '__main__':
    assistant = VoiceAssistant()
    assistant.run()