import pyttsx3  # Text-to-Speech library
import speech_recognition as sr  # Voice Recognition library
import json

# Initialize text-to-speech engine
def init_tts():
    tts = pyttsx3.init()
    # Set properties for better sound quality
    tts.setProperty('rate', 150)  # Speed
    tts.setProperty('volume', 1)  # Volume 0-1
    return tts

# Function for multilingual support

def speak(text, lang='en'):
    tts = init_tts()
    if lang == 'ru':
        # Set to Russian voice if available
        voices = tts.getProperty('voices')
        tts.setProperty('voice', voices[1].id)  # Assuming Russian is the second voice.
    tts.say(text)
    tts.runAndWait()

# Improved voice recognition method with emotion detection in Russian
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
        text = r.recognize_google(audio, language='ru-RU')  # Using Russian for recognition
        print(f'Recognized: {text}')
        return text

# Main function
if __name__ == '__main__':
    while True:
        try:
            spoken_text = recognize_speech()
            # Placeholder for emotion detection logic...
            # Process the recognized text
            speak('Вы сказали: ' + spoken_text, lang='ru')
        except sr.UnknownValueError:
            print('Could not understand audio')
        except sr.RequestError as e:
            print(f'Could not request results; {e}')