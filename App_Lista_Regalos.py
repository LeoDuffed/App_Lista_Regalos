from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

storage = JsonStore("lista_regalos.jason")

class PantallaInicio(Screen):
    def __init__(self, **kawargs):
        regalos().__init__(**kawargs)

        layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)

class ListaRegalos(App):
    def build(self):

        return sm


ListaRegalos().run()