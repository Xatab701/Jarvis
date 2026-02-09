import speech_recognition as sr
import pyttsx3
import openai
import requests
import datetime
from typing import Dict

class NameDeclension:
    """Класс для склонения имён по падежам русского языка"""
    
    def __init__(self):
        self.declensions = {
            'именительный': 'Дима',      # Кто? Что?
            'родительный': 'Димы',        # Кого? Чего?
            'дательный': 'Диме',          # Кому? Чему?
            'винительный': 'Диму',        # Кого? Что?
            'творительный': 'Димой',      # Кем? Чем?
            'предложный': 'Диме'          # О ком? О чём?
        }
    
    def get_form(self, case: str) -> str:
        """Получить форму имени в нужном падеже"""
        return self.declensions.get(case, 'Дима')

class JarvisAssistant:
    def __init__(self, user_name: str = "Дима"):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.recognizer = sr.Recognizer()
        self.user_name = user_name
        self.name_declension = NameDeclension()
        
    def speak(self, text: str):
        """Озвучить текст"""
        print(f"🤖 Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self) -> str:
        """Слушать голосовую команду"""
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("🎤 Слушаю...")
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio, language='ru-RU')
                print(f"👤 Вы: {command}")
                return command.lower()
        except sr.UnknownValueError:
            self.speak("Извините, я не смог разобрать вашу речь")
            return ""
        except sr.RequestError:
            self.speak("Ошибка при подключении к Google Speech Recognition")
            return ""
    
    def greet_user(self):
        """Приветствие пользователя"""
        name_nominative = self.name_declension.get_form('именительный')
        greeting = f"Привет, {name_nominative}! Я Jarvis. Чем я могу тебе помочь?"
        self.speak(greeting)
    
    def call_user_nominative(self):
        """Позвать пользователя в именительном падеже"""
        name = self.name_declension.get_form('именительный')
        self.speak(f"{name}, я здесь!")
    
    def call_user_genitive(self):
        """Упомянуть пользователя в родительном падеже"""
        name = self.name_declension.get_form('родительный')
        self.speak(f"Я видел {name} в офисе")
    
    def call_user_dative(self):
        """Обратиться к пользователю в дательном падеже"""
        name = self.name_declension.get_form('дательный')
        self.speak(f"Что я могу сделать для {name}?")
    
    def call_user_accusative(self):
        """Упомянуть пользователя в винительном падеже"""
        name = self.name_declension.get_form('винительный')
        self.speak(f"Я вижу {name}")
    
    def call_user_instrumental(self):
        """Упомянуть пользователя в творительном падеже"""
        name = self.name_declension.get_form('творительный')
        self.speak(f"Рад работать с {name}")
    
    def call_user_prepositional(self):
        """Упомянуть пользователя в предложном падеже"""
        name = self.name_declension.get_form('предложный')
        self.speak(f"Я думаю о {name}")
    
    def tell_time(self):
        """Сказать текущее время"""
        now = datetime.datetime.now()
        hours = now.hour
        minutes = now.minute
        name = self.name_declension.get_form('именительный')
        
        time_str = f"{hours}:{minutes:02d}"
        self.speak(f"{name}, текущее время {time_str}")
    
    def tell_date(self):
        """Сказать текущую дату"""
        now = datetime.datetime.now()
        date_str = now.strftime('%d.%m.%Y')
        day_name = self._get_day_name(now.weekday())
        name = self.name_declension.get_form('именительный')
        
        self.speak(f"{name}, сегодня {day_name}, {date_str}")
    
    def _get_day_name(self, weekday: int) -> str:
        """Получить название дня недели"""
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        return days[weekday]
    
    def get_weather(self, city: str = "Москва"):
        """Получить информацию о погоде"""
        try:
            api_key = 'your_api_key'
            base_url = 'http://api.openweathermap.org/data/2.5/weather'
            params = {'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'ru'}
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                name = self.name_declension.get_form('именительный')
                
                self.speak(f"{name}, погода в городе {city}: {description}, температура {temp} градусов по Цельсию")
            else:
                self.speak("Не удалось получить информацию о погоде")
        except Exception as e:
            self.speak(f"Ошибка при получении информации о погоде: {str(e)}")
    
    def main_loop(self):
        """Основной цикл работы ассистента"""
        self.greet_user()
        
        while True:
            command = self.listen()
            
            if not command:
                continue
            
            # Команды с упоминанием имени в разных падежах
            if 'время' in command:
                self.tell_time()
            elif 'дата' in command:
                self.tell_date()
            elif 'погода' in command:
                self.get_weather()
            elif 'позови' in command:
                self.call_user_nominative()
            elif 'спасибо' in command or 'благодарю' in command:
                name = self.name_declension.get_form('дательный')
                self.speak(f"Мне приятно помочь {name}!")
            elif 'как' in command and 'дела' in command:
                name = self.name_declension.get_form('дательный')
                self.speak(f"Спасибо за внимание, {name}! Все работает отлично!")
            elif 'стоп' in command or 'выход' in command or 'пока' in command:
                name = self.name_declension.get_form('именительный')
                self.speak(f"До свидания, {name}! Был рад помочь!")
                break
            else:
                name = self.name_declension.get_form('дательный')
                self.speak(f"Извините, {name}, я не понимаю эту команду. Попробуйте ещё раз.")

if __name__ == '__main__':
    assistant = JarvisAssistant(user_name="Дима")
    assistant.main_loop()