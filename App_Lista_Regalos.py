#Creado por Leonardo Martinez Peña

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

storage = JsonStore("lista_regalos.jason")

class Pantalla_Inicio(Screen):
    def __init__(self, **kawargs):
        super().__init__(**kawargs)

        layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)

        welcomerLabel = Label (text = "Tus listas de regalos", font_size = '30sp', color = (0,0,0,1))
        layout.add_widget(welcomerLabel)

        boton_pantalla_personas = Button(text = "Inicia tu lista", pos_hint = {"center_x": 0.5}, background_color = (0.5,1,0,1))
        boton_pantalla_personas.bind(on_press = self.CambiarPersonas)
        layout.add_widget(boton_pantalla_personas)

        boton_agregar_personas = Button(text = "Agrega personas",pos_hint = {"center_x": 0.5}, background_color = (0.5,1,0,1) )
        boton_agregar_personas.bind(on_press = self.Cambiar_Agregar_Peronas)
        layout.add_widget(boton_agregar_personas)

        self.add_widget(layout)

    def CambiarPersonas(self, instance):
        self.manager.current = 'listaIni'

    def Cambiar_Agregar_Peronas(self, instance):
        self.manager.current = 'AddPerson'

                                         

class Pantalla_Aniadir_Lista_Personas(Screen):
    def __init__(self, **k):
        super().__init__(**k)

        Window.clearcolor = (1, 1, 0.9, 1)

        layout = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)

        welcomerLabel = Label (text = "Crea tus listas", font_size = '30sp', color = (0,0,0,1))
        layout.add_widget(welcomerLabel)

        self.scroll = ScrollView(size_hint = (1, 0.8))
        self.lista_personas = BoxLayout(orientation = 'vertical', size_hint_y = None)
        self.lista_personas.bind(minimum_height = self.lista_personas.setter('height'))
        self.scroll.add_widget(self.lista_personas)
        layout.add_widget(self.scroll)

        input_data = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.name_input = TextInput(hint_text = "Nombre de la persona", multiline = False)
        self.regalos_cont_input = TextInput(hint_text = "Numero de regalos", multiline = False)
        add_person_button = Button(text = "Añadir persona", on_press = self.add_person) # falta el add person 
        input_data.add_widget(self.name_input)
        input_data.add_widget(self.regalos_cont_input)
        input_data.add_widget(add_person_button)
        layout.add_widget(input_data)

        boton_volver = Button(text = "Volver", pos_hint = {"center_x":0.5}, background_color = (1, 0.7, 0.8, 1))
        boton_volver.bind(on_press = self.CambiarVolver)
        layout.add_widget(boton_volver)

        self.add_widget(layout)

    def add_person(self, instance): 
        nombre = self.name_input.text.strip()
        cont_regalos = self.regalos_cont_input.text.strip()
        
        if nombre and cont_regalos.isdigit():
            cont_regalos = int(cont_regalos)
            personas_layout = BoxLayout(size_hint_y = None, height = 50, spacing = 10)

            nombre_label = Label(text = nombre, size_hint_x = 0.3, color = (0,0,0,1))

            barra_progreso = ProgressBar(max = cont_regalos, size_hint_x = 0.3)

            add_gift_button = Button(text = "+1 Regalo", size_hint_x = 0.2)
            add_gift_button.bind (on_press = lambda btn: self.update_progress(barra_progreso))

            personas_layout.add_widget(nombre_label)
            personas_layout.add_widget(barra_progreso)
            personas_layout.add_widget(add_gift_button)
            self.lista_personas.add_widget(personas_layout)
            self.name_input.text = " "
            self.regalos_cont_input.text = ""
        
    def update_progress(self, barra_progreso): 
        if barra_progreso.value < barra_progreso.max: 
            barra_progreso.value += 1


    def CambiarVolver(self, instance):
        self.manager.current = "inicio"

class Personas_Regalos_Main_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)

        instruction_label = Label (text = "Agrega a las personas", font_size = '25sp', color = (0,0,0,1))
        self.layout.add_widget(instruction_label)

        self.scroll = ScrollView(size_hint = (1,0.8))
        self.lista_personas = BoxLayout(orientation = 'vertical', size_hint_y = None)
        self.lista_personas.bind(minimum_height = self.lista_personas.setter('height'))
        self.scroll.add_widget(self.lista_personas)
        self.layout.add_widget(self.scroll)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.nombre_input = TextInput(hint_text = "Nombre de la persona", multiline = False)
        add_person_button = Button(text = "Agregar persona", on_press = self.add_person)
        input_area.add_widget(self.nombre_input)
        input_area.add_widget(add_person_button)
        self.layout.add_widget(input_area)

        boton_volver = Button(text = "Volver", pos_hint = {"center_x":0.5}, background_color = (1, 0.7, 0.8, 1))
        boton_volver.bind(on_press = self.CambiarVolver)
        self.layout.add_widget(boton_volver)

        self.add_widget(self.layout)

    def CambiarVolver(self, instance): 
        self.manager.current = 'listaIni'
    
    def add_person(self, instance):
        nombre = self.nombre_input.text.strip()
        if nombre: 
            persona_button = Button(text = nombre, size_hint_y = None, height = 50)
            persona_button.bind(on_press = lambda btn: self.open_person_screen(nombre))
            self.lista_personas.add_widget(persona_button)
            self.nombre_input.text = ""

    def open_person_screen(self, nombre):
        app = App.get_running_app()
        persona_screen = app.root.get_screen('person_screen')
        persona_screen.set_person_name(nombre)
        app.root.transition = SlideTransition(direction = "left")
        app.root.current = 'person_screen'

class Editar_Personas(Screen):
    def __init__(self, **kw): 
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        self.add_widget(self.layout)

        self.persona_label = Label(text = "", size_hint = (1, 0.1), font_size = "20sp", color = (0,0,0,1))
        self.layout.add_widget(self.persona_label)

        self.scroll = ScrollView(size_hint = (1, 0.8))
        self.checklist = BoxLayout(orientation = 'vertical', size_hint_y = None, spacing = 10)
        self.checklist.bind(minimum_height = self.checklist.setter("height"))
        self.scroll.add_widget(self.checklist)
        self.layout.add_widget(self.scroll)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.regalo_input = TextInput(hint_text = "Ingresa regalo", multiline = False)
        agreagar_button = Button(text = "Añadir", on_press = self.add_item)
        input_area.add_widget(self.regalo_input)
        input_area.add_widget(agreagar_button)
        self.layout.add_widget(input_area)

        boton_volver = Button(text = "Volver", pos_hint = {"center_x":0.5}, background_color = (1, 0.7, 0.8, 1))
        boton_volver.bind(on_press = self.CambiarVolver)
        self.layout.add_widget(boton_volver)

    def set_person_name(self, name): 
        self.persona_label.text = f"Regalos para {name}"
        self.checklist.clear_widgets()

    def CambiarVolver(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="right")
        app.root.current = "AddPerson"

    def add_item(self, instance): 

        gift_text = self.regalo_input.text.strip()

        if gift_text: 
            
            gift_layout = BoxLayout(size_hint_y = None, height = 40, spacing = 10)
            checkbox = CheckBox(size_hint_x =0.1)
            regalo_label = Label(text = gift_text, size_hint_x = 0.8, color = (0,0,0,1))
            delete_button = Button(text = "Eliminar", size_hint_x = 0.1)
            delete_button.bind(on_press = lambda btn: self.remove_gift(gift_layout))

            gift_layout.add_widget(checkbox)
            gift_layout.add_widget(regalo_label)
            gift_layout.add_widget(delete_button)
            self.checklist.add_widget(gift_layout)
            self.regalo_input.text = " "

    def remove_gift(self, item_layout): 
        self.checklist.remove_widget(item_layout)


class Lista_Regalos(App):
    def build(self):
        
        sm = ScreenManager()
        sm.add_widget(Pantalla_Inicio(name = 'inicio'))
        sm.add_widget(Pantalla_Aniadir_Lista_Personas(name = 'listaIni'))
        sm.add_widget(Personas_Regalos_Main_Screen(name = 'AddPerson'))
        sm.add_widget(Editar_Personas(name = 'person_screen'))
        return sm


Lista_Regalos().run()