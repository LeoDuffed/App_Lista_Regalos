#Creado por Leonardo Martinez Peña

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.base import EventLoop
from kivy.utils import platform
from kivy.core.window import Window

storage = JsonStore("lista_regalos.jason")


class Pantalla_Inicio(Screen):
    def __init__(self, **kawargs):
        super().__init__(**kawargs)

        main_layout = FloatLayout()

        layout = BoxLayout(orientation = 'vertical', padding = (10,50), spacing = 20)

        reset_button = Button(text = "Reset", size_hint = (0.2,0.05), pos_hint = {'right': 1, 'top': 1})
        reset_button.bind(on_release = self.reset_lists_buttons)
        main_layout.add_widget(reset_button)

        welcomerLabel = Label (text = "Tus listas de regalos", font_size = '30sp', color = (0,0,0,1), halign = 'center', size_hint_y = 0.2)
        layout.add_widget(welcomerLabel)

        boton_pantalla_presupuesto = Button(text = "Tu presupuesto", pos_hint = {"center_x": 0.5}, background_color = (0.5,1,0,1), size_hint = (0.92, None), height = 200, font_size = '20sp')
        boton_pantalla_presupuesto.bind(on_press = self.Cambiar_Presupuesto)
        layout.add_widget(boton_pantalla_presupuesto)

        boton_pantalla_personas = Button(text = "Inicia tu lista", pos_hint = {"center_x": 0.5}, background_color = (0.5,1,0,1), size_hint = (0.92, None), height = 200, font_size = '20sp')
        boton_pantalla_personas.bind(on_press = self.CambiarPersonas)
        layout.add_widget(boton_pantalla_personas)

        boton_agregar_personas = Button(text = "Agrega personas",pos_hint = {"center_x": 0.5}, background_color = (0.5,1,0,1), size_hint = (0.92, None), height = 200, font_size = '20sp' )
        boton_agregar_personas.bind(on_press = self.Cambiar_Agregar_Peronas)
        layout.add_widget(boton_agregar_personas)

        main_layout.add_widget(layout)

        self.add_widget(main_layout)

    def reset_lists_buttons(self, instance): 
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        mensaje = Label(text="¿Estás seguro de que quieres reiniciar la app?\nEsta acción borrará todos los datos.", size_hint_y=0.6, font_size = '13sp')
        content.add_widget(mensaje)

        botones = BoxLayout(size_hint_y=0.4, spacing=10)

        boton_confirmar = Button(text="Confirmar", background_color=(0, 1, 0, 1))
        boton_confirmar.bind(on_press=self.reset,on_release=lambda x: popup.dismiss() )
        botones.add_widget(boton_confirmar)

        close_button = Button(text="Cancelar", background_color=(1, 0, 0, 1))
        close_button.bind(on_release=lambda x: popup.dismiss())
        botones.add_widget(close_button)

        content.add_widget(botones)

        popup = Popup(title="Reiniciar App", content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        popup.open()

    def reset(self, instance):
        storage.clear()

        app = App.get_running_app()
        for screen in app.root.screens:
            if hasattr(screen, "lista_personas"):
                screen.lista_personas.clear_widgets()

        presupuesto_screen = app.root.get_screen('presupuesto')
        presupuesto_screen.presupuesto_inicial.text = "Presupuesto no definido"
        presupuesto_screen.update_budget_label(0)
    
    def Cambiar_Presupuesto(self, instance): 
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left") 
        self.manager.current = 'presupuesto'
                
    def CambiarPersonas(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left") 
        self.manager.current = 'listaIni'

    def Cambiar_Agregar_Peronas(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left") 
        self.manager.current = 'AddPerson'
                            

class Pantalla_Presupuesto(Screen): 
    def __init__(self, **kw): 
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding= (10, 50, 10,10), spacing = 10)

        welcome_label = Label(text = "Mantengase al dia\ncon su presupuesto", font_size = '30sp', color = (0,0,0,1), halign = 'center', size_hint_y = 0.2)
        self.layout.add_widget(welcome_label)

        self.presupuesto_inicial = Label(text = "", font_size = '20sp', color = (0,0,0,1), halign = 'center')
        self.layout.add_widget(self.presupuesto_inicial)

        input_budget = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.budget_input = TextInput(hint_text = "Ingrese su presupuesto", multiline = False)
        add_budget_button = Button(text = "Añadir presupuesto", on_press = self.add_presupuesto)
        input_budget.add_widget(self.budget_input)
        input_budget.add_widget(add_budget_button)
        self.layout.add_widget(input_budget)

        input_gasto_layout = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.gasto_input = TextInput(hint_text = "Ingrese lo gastado", multiline = False)
        add_gasto_button = Button(text = "Agrega gasto", on_press = self.sub_gasto)
        input_gasto_layout.add_widget(self.gasto_input)
        input_gasto_layout.add_widget(add_gasto_button)
        self.layout.add_widget(input_gasto_layout) 

        self.budget_track_label = Label(text = "", font_size = '25sp', color = (0,0,0,1), halign = 'center')
        self.layout.add_widget(self.budget_track_label)

        self.add_widget(self.layout)

        self.load_budget(self)

    def add_presupuesto(self, instance): 

        try: 
            budget = float(self.budget_input.text)
            storage.put("budget", total = budget, initial = budget)
            self.presupuesto_inicial.text = f"Presupuesto inicial: ${budget:.2f}"
            self.update_budget_label(budget)
            self.budget_input.text = ""
        except ValueError: 
            self.budget_track_label.text = "Error: Ingrese un numero valido"
            return 
        
    def sub_gasto(self, instance): 

        try: 
            gasto = float(self.gasto_input.text)
        except ValueError: 
            self.budget_track_label.text = "Error: Ingrese un numero valido"
            return 

        if storage.exists("budget"): 
            budget = storage.get("budget")["total"]
        else: 
            budget = 0

        if gasto > budget: 
            self.budget_track_label.text = "Se acabo tu presupuesto"
        else: 
            budget -= gasto
            storage.put("budget", total = budget)
            self.update_budget_label(budget)

        self.gasto_input.text = ""

    def load_budget(self, instance): 
        if storage.exists("budget"): 
            data = storage.get("budget")
            initial_budget = data.get("initial","Presupuesto inicial no definido")
            total_budget = data["total"]
            self.presupuesto_inicial.text = f"Presupuesto incial: ${initial_budget}"
            self.update_budget_label(total_budget)
        else: 
            self.presupuesto_inicial.text = "Presupuesto inicial no definido"
            self.update_budget_label(0)

    def update_budget_label(self, budget): 
        self.budget_track_label.text = f"Presupuesto: ${budget:.2f}"

    def on_touch_move(self, touch):
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'inicio'


class Pantalla_Aniadir_Lista_Personas(Screen):
    def __init__(self, **k):
        super().__init__(**k)

        Window.clearcolor = (1, 1, 0.9, 1)

        layout = BoxLayout(orientation = 'vertical', padding = (10, 50,10,30), spacing = 10)

        welcomerLabel = Label (text = "Crea tus listas", font_size = '30sp', color = (0,0,0,1), halign = 'center', size_hint_y = 0.2)
        layout.add_widget(welcomerLabel)

        input_data = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.name_input = TextInput(hint_text = "Nombre de la persona", multiline = False)
        self.regalos_cont_input = TextInput(hint_text = "Numero de regalos", multiline = False)
        add_person_button = Button(text = "Añadir persona", on_press = self.add_person)  
        input_data.add_widget(self.name_input)
        input_data.add_widget(self.regalos_cont_input)
        input_data.add_widget(add_person_button)
        layout.add_widget(input_data)

        scroll_container = AnchorLayout(size_hint = (1, 0.8))
        self.scroll = ScrollView(size_hint = (None, 0.8), size = (600, 400))
        self.lista_personas = BoxLayout(orientation = 'vertical', size_hint_y = None,size_hint_x = 1, padding = (10, 40, 10,10), spacing = 10)
        self.lista_personas.bind(minimum_height = self.lista_personas.setter('height'))
        self.scroll.add_widget(self.lista_personas)
        scroll_container.add_widget(self.scroll)
        layout.add_widget(scroll_container)

        self.add_widget(layout)

        self.load_personas()

    def add_person(self, instance):
        nombre = self.name_input.text.strip()
        cont_regalos = self.regalos_cont_input.text.strip()

        if nombre and cont_regalos.isdigit():
            cont_regalos = int(cont_regalos)

            personas_layout = self.create_person_layout(nombre, cont_regalos, 0)  
            self.lista_personas.add_widget(personas_layout)

            if not storage.exists("personas"):
                storage.put("personas", lista=[])
            personas = storage.get("personas")["lista"]
            personas.append({"nombre": nombre, "max_regalos": cont_regalos, "progreso": 0})
            storage.put("personas", lista=personas)

            self.name_input.text = ""
            self.regalos_cont_input.text = ""

    def load_personas(self):
        if storage.exists("personas"):
            personas = storage.get("personas")["lista"]
            for persona in personas:
                personas_layout = self.create_person_layout(
                    persona["nombre"], persona["max_regalos"], persona["progreso"]
                )
                self.lista_personas.add_widget(personas_layout)

    def create_person_layout(self, nombre, max_regalos, progreso):
        personas_layout = BoxLayout(size_hint=(1, None),width = 800, height=50, spacing=10, padding = (10,30,10,10))

        nombre_label = Label(text=nombre, size_hint = (0, 5), color=(0, 0, 0, 1), font_size = '18sp', halign = 'left', valign = 'middle')
        sub_gift_button = Button(text = "-1", size_hint = (None, None), width = 50, height = 50)
        barra_progreso = ProgressBar(max=max_regalos, value=progreso, size_hint = (None, 5), width = 200, height = 30)
        add_gift_button = Button(text="+1", size_hint = (None, None), width = 50, height = 50)
        delet_button = Button(text = "Eliminar", size_hint = (None, None), width = 100, height = 50)
        sub_gift_button.bind(on_press = lambda btn: self.sub_progress(barra_progreso, nombre))
        add_gift_button.bind(on_press=lambda btn: self.add_progress(barra_progreso, nombre))
        delet_button.bind(on_press = lambda btn:self.remove_person(personas_layout, nombre))

        personas_layout.add_widget(nombre_label)
        personas_layout.add_widget(sub_gift_button)
        personas_layout.add_widget(barra_progreso)
        personas_layout.add_widget(add_gift_button)
        personas_layout.add_widget(delet_button)

        return personas_layout
    
    def remove_person(self,layout, nombre):
        self.lista_personas.remove_widget(layout)

        if storage.exists("personas"): 
            personas = storage.get("personas")["lista"]
            personas = [personas for persona in personas if persona ["nombre"] != nombre]
            storage.put("personas", lista= personas)

    def sub_progress(self, barra_progreso, nombre): 
        if barra_progreso.value < barra_progreso.max:
            barra_progreso.value -= 1

            personas = storage.get("personas")["lista"]
            for persona in personas:
                if persona["nombre"] == nombre:
                    persona["progreso"] = barra_progreso.value
                    break
            storage.put("personas", lista=personas)

    def add_progress(self, barra_progreso, nombre):
        if barra_progreso.value < barra_progreso.max:
            barra_progreso.value += 1

            personas = storage.get("personas")["lista"]
            for persona in personas:
                if persona["nombre"] == nombre:
                    persona["progreso"] = barra_progreso.value
                    break
            storage.put("personas", lista=personas)

    def on_touch_move(self, touch): 
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'inicio'


class Personas_Regalos_Main_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = (10, 50,10,30), spacing = 10)

        instruction_label = Label (text = "Agrega a las personas", font_size = '30sp', color = (0,0,0,1), size_hint_y = 0.3)
        self.layout.add_widget(instruction_label)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.nombre_input = TextInput(hint_text = "Nombre de la persona", multiline = False)
        add_person_button = Button(text = "Agregar persona", on_press = self.add_person)
        input_area.add_widget(self.nombre_input)
        input_area.add_widget(add_person_button)
        self.layout.add_widget(input_area)

        self.scroll = ScrollView(size_hint = (1,0.8))
        self.lista_personas = BoxLayout(orientation = 'vertical', size_hint_y = None)
        self.lista_personas.bind(minimum_height = self.lista_personas.setter('height'))
        self.scroll.add_widget(self.lista_personas)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)
    
        self.load_personas()

    def load_personas(self): 
        for persona in storage.keys(): 
            if persona == "personas": 
                continue
            if persona == "budget":
                continue

            self.add_person_to_list(persona)

    def add_person_to_list(self, nombre): 
        persona_button = Button(text = nombre, pos_hint = {"center_x": 0.5}, size_hint = (0.92, None), height = 90, font_size = '20sp')
        persona_button.bind(on_press = lambda btn: self.open_person_screen(nombre))
        self.lista_personas.add_widget(persona_button)
    
    def add_person(self, instance):
        nombre = self.nombre_input.text.strip()
        if nombre: 
            persona_button = Button(text = nombre,  pos_hint = {"center_x": 0.5}, size_hint = (0.92, None), height = 90, font_size = '20sp')
            persona_button.bind(on_press = lambda btn: self.open_person_screen(nombre))
            self.lista_personas.add_widget(persona_button)
            self.nombre_input.text = ""

    def open_person_screen(self, nombre):
        app = App.get_running_app()
        persona_screen = app.root.get_screen('person_screen')
        persona_screen.set_person_name(nombre)
        app.root.transition = SlideTransition(direction = "left")
        app.root.current = 'person_screen'
    
    def on_touch_move(self, touch): 
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'inicio'


class Editar_Personas(Screen):
    def __init__(self, **kw): 
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = 10, spacing = 10)
        self.add_widget(self.layout)

        self.persona_label = Label(text = "", size_hint = (1, 0.1), font_size = "20sp", color = (0,0,0,1))
        self.layout.add_widget(self.persona_label)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10)
        self.regalo_input = TextInput(hint_text = "Ingresa regalo", multiline = False)
        agreagar_button = Button(text = "Añadir", on_press = self.add_item)
        input_area.add_widget(self.regalo_input)
        input_area.add_widget(agreagar_button)
        self.layout.add_widget(input_area)

        self.scroll = ScrollView(size_hint = (1, 0.8))
        self.checklist = BoxLayout(orientation = 'vertical', size_hint_y = None, spacing = 10)
        self.checklist.bind(minimum_height = self.checklist.setter("height"))
        self.scroll.add_widget(self.checklist)
        self.layout.add_widget(self.scroll)

    def set_person_name(self, name):
        self.persona_label.text = f"Regalos para {name}"
        self.checklist.clear_widgets()

        if storage.exists(name):
            regalos = storage.get(name)['regalos']
            for regalo in regalos:
                if isinstance(regalo, dict):
                    gift_layout = self.create_gift_widget(regalo["nombre"], regalo.get("marcado", False))
                else:
                    gift_layout = self.create_gift_widget(regalo, False)
                self.checklist.add_widget(gift_layout)

    def create_gift_widget(self, gift_text, marcado):
        gift_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

        checkbox = CheckBox(size_hint_x=0.1, active=marcado)
        checkbox.bind(on_release=lambda cb: self.update_gift_status(gift_text, cb.active))

        regalo_label = Label(text=gift_text, size_hint_x=0.8, color=(0, 0, 0, 1))
        delete_button = Button(text="Eliminar", size_hint_x=0.1)
        delete_button.bind(on_press=lambda btn: self.remove_gift(gift_layout, gift_text))

        gift_layout.add_widget(checkbox)
        gift_layout.add_widget(regalo_label)
        gift_layout.add_widget(delete_button)
        return gift_layout

    def update_gift_status(self, gift_text, marcado):
        persona = self.persona_label.text.replace("Regalos para ", "").strip()
        if storage.exists(persona):
            regalos = storage.get(persona)['regalos']
            for regalo in regalos:
                if isinstance(regalo, dict) and regalo["nombre"] == gift_text:
                    regalo["marcado"] = marcado
                    break
            storage.put(persona, regalos=regalos)

    def add_item(self, instance):
        gift_text = self.regalo_input.text.strip()

        if gift_text:
            persona = self.persona_label.text.replace("Regalos para ", "").strip()

            gift_layout = self.create_gift_widget(gift_text, False)
            self.checklist.add_widget(gift_layout)

            if not storage.exists(persona):
                storage.put(persona, regalos=[])
            regalos = storage.get(persona)['regalos']
            regalos.append({"nombre": gift_text, "marcado": False})
            storage.put(persona, regalos=regalos)

            self.regalo_input.text = ""

    def remove_gift(self, item_layout, gift_text):
        self.checklist.remove_widget(item_layout)

        persona = self.persona_label.text.replace("Regalos para ", "").strip()
        if storage.exists(persona):
            regalos = storage.get(persona)['regalos']
            regalos = [regalo for regalo in regalos if isinstance(regalo, dict) and regalo["nombre"] != gift_text]
            storage.put(persona, regalos=regalos)
    
    def on_touch_move(self, touch): 
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'AddPerson'


class Lista_Regalos(App):
    def build(self):
        
        sm = ScreenManager()
        sm.add_widget(Pantalla_Inicio(name = 'inicio'))
        sm.add_widget(Pantalla_Presupuesto(name = 'presupuesto'))
        sm.add_widget(Pantalla_Aniadir_Lista_Personas(name = 'listaIni'))
        sm.add_widget(Personas_Regalos_Main_Screen(name = 'AddPerson'))
        sm.add_widget(Editar_Personas(name = 'person_screen'))

        if platform == 'android': 
            EventLoop.window.bind(on_keyboard = self.android_back_button)

        return sm
    def android_back_button(self, window, key, *args): 
        if key == 27: 
            screen_manager = self.root
            if screen_manager.current != 'inicio': 
                screen_manager.current = 'inicio'
                return True
            return False

    
    def on_stop(self):
        return super().on_stop()


Lista_Regalos().run()