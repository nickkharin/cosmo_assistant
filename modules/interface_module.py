import sys
import tkinter as tk
from tkinter import simpledialog, messagebox


class InterfaceModule:
    def __init__(self, language='ru', mode='text'):
        self.language = language
        self.mode = mode
        self.translations = {
            'en': {
                'greeting': 'Hello, please write your username',
                'farewell': 'Goodbye!'
            },
            'ru': {
                'greeting': 'Привет, пожалуйста назовите свой логин',
                'farewell': 'До свидания!'
            }
        }

    def get_user_input(self):
        if self.mode == 'text':
            return input("User: ")
        elif self.mode == 'gui':
            self._init_gui()
            greeting = self.translations[self.language]['greeting']
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

