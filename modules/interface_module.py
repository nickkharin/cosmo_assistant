import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import speech_recognition as sr
import pyttsx3

class InterfaceModule:
    def __init__(self, language='en', mode='text'):
        self.language = language
        self.mode = mode
        self.engine = pyttsx3.init()
        self.translations = {
            'en': {
                'greeting': 'Hello, how can I assist you today?',
                'farewell': 'Goodbye!'
            },
            'ru': {
                'greeting': 'Привет, чем я могу помочь сегодня?',
                'farewell': 'До свидания!'
            }
        }

    def get_user_input(self):
        if self.language not in self.translations:
            self.language = 'en'  # Default to English if unsupported language is set
        greeting = self.translations[self.language]['greeting']

        if self.mode == 'text':
            print(greeting)
            return input("User: ")
        elif self.mode == 'gui':
            self._init_gui()
            return simpledialog.askstring("Input", greeting)
        elif self.mode == 'voice':
            return self._get_voice_input()

    def display_text(self, text):
        if self.mode == 'text':
            print(f"Cosmo: {text}")
        elif self.mode == 'gui':
            messagebox.showinfo("Cosmo", text)
        elif self.mode == 'voice':
            self._speak(text)

    def change_language(self, language):
        if language in self.translations:
            self.language = language
        else:
            print("Language not supported.")

    def display_farewell(self):
        farewell = self.translations[self.language]['farewell']
        self.display_text(farewell)

    def _init_gui(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window

    def _get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return "Could not request results; {0}".format(e)

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

# Example usage
interface = InterfaceModule(language='ru', mode='voice')
user_input = interface.get_user_input()
interface.display_text("Это пример ответа.")
interface.display_farewell()
