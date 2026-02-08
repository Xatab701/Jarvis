import speech_recognition as sr
import pyttsx3
import openai
import os

# Инициализация OpenAI
openai.api_key = 'YOUR_API_KEY'

# Инициализация двигателя для текстовой речи
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-нибудь:")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='ru-RU')
            return command
        except sr.UnknownValueError:
            print("Не удалось распознать звук")
            return None
        except sr.RequestError:
            print("Не удается получить результаты из Google Speech Recognition")
            return None

def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    while True:
        command = listen()
        if command:
            print(f"Вы сказали: {command}")
            if 'выход' in command:
                speak("До свидания!")
                break
            elif 'сказать' in command:
                text = command.replace('сказать', '').strip()
                speak(text)
            elif 'выполнить' in command:
                os.system(command.replace('выполнить', '').strip())
            else:
                response = chatgpt_response(command)
                print(response)
                speak(response)
