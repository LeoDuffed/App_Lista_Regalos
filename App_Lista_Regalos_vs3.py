#Creado por Leonardo Martinez Peña

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.base import EventLoop
from kivy.utils import platform
from kivy.core.window import Window


storage = JsonStore("lista_regalos.jason")


class Pantalla_Inicio(Screen):
    def __init__(self, **kawargs):
        super().__init__(**kawargs)

        Window.clearcolor = (1,1,1,1)


        main_layout = FloatLayout()

        layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 10)

        reset_button = Button(text = "Reset", size_hint = (0.3,0.05), pos_hint = {'right': 1, 'top': 1})
        reset_button.bind(on_release = self.reset_lists_buttons)
        main_layout.add_widget(reset_button)

        welcomerLabel = Label (text = "", font_size = '30sp', color = (0,0,0,1))
        welcomerLabel.markup = True
        welcomerLabel.text = f"[b]Tus listas de regalos[/b]"
        layout.add_widget(welcomerLabel)

        boton_pantalla_presupuesto = Button(text = "Tu presupuesto", pos_hint = {"center_x": 0.5}, size_hint_x = 0.92, font_size = '20sp')
        boton_pantalla_presupuesto.bind(on_press = self.Cambiar_Presupuesto)
        layout.add_widget(boton_pantalla_presupuesto)

        boton_agregar_personas = Button(text = "Agrega personas",pos_hint = {"center_x": 0.5}, size_hint_x = 0.92, font_size = '20sp')
        boton_agregar_personas.bind(on_press = self.Cambiar_Agregar_Peronas)
        layout.add_widget(boton_agregar_personas)

        main_layout.add_widget(layout)

        self.add_widget(main_layout)

    def reset_lists_buttons(self, instance): 
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        mensaje = Label(text="¿Estás seguro de que quieres reiniciar la app?\nEsta acción borrará todos los datos.", size_hint_y=0.6, font_size = '13sp')
        content.add_widget(mensaje)

        botones = BoxLayout(size_hint_y=0.4, spacing=10)

        boton_confirmar = Button(text="Confirmar")
        boton_confirmar.bind(on_press=self.reset,on_release=lambda x: popup.dismiss() )
        botones.add_widget(boton_confirmar)

        close_button = Button(text="Cancelar")
        close_button.bind(on_release=lambda x: popup.dismiss())
        botones.add_widget(close_button)

        content.add_widget(botones)

        popup = Popup(title="Reiniciar App", content=content, size_hint=(0.9, 0.5), auto_dismiss=False)
        popup.open()

    def reset(self, instance):
        storage.clear()

        app = App.get_running_app()
        for screen in app.root.screens:
            if hasattr(screen, "lista_personas"):
                screen.lista_personas.clear_widgets()
            if hasattr(screen, "check_anio_pasado"):
                screen.check_anio_pasado.active = False
            if hasattr(screen, "barra_progreso"):
                screen.barra_progreso.max = 0
                screen.barra_progreso.value = 0

        presupuesto_screen = app.root.get_screen('presupuesto')
        presupuesto_screen.presupuesto_inicial.text = "Presupuesto no definido"
        presupuesto_screen.update_budget_label(0)
    
    def Cambiar_Presupuesto(self, instance): 
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left") 
        self.manager.current = 'presupuesto'

    def Cambiar_Agregar_Peronas(self, instance):
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left") 
        self.manager.current = 'AddPerson'
                            

class Pantalla_Presupuesto(Screen): 
    def __init__(self, **kw): 
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = (10, 50,10,10), spacing = 10)

        welcome_label = Label(text = "", font_size = '30sp', color = (0,0,0,1), halign = 'center', size_hint_y = 0.2)
        welcome_label.markup= True
        welcome_label.text = f"[b]Mantengase al dia\ncon su presupuesto[/b]"
        self.layout.add_widget(welcome_label)

        self.presupuesto_inicial = Label(text = "", font_size = '20sp', color = (0,0,0,1), halign = 'center', height = 30, size_hint_y = 0.2)
        self.layout.add_widget(self.presupuesto_inicial)

        input_budget = BoxLayout(size_hint = (1, 0.2), spacing = 10, size_hint_y = 0.2, padding = (50,3,50,3))
        self.budget_input = TextInput(hint_text = "Ingrese su presupuesto", multiline = False, height = 150)
        add_budget_button = Button(text = "Añadir presupuesto", on_press = self.add_presupuesto, height = 150)
        input_budget.add_widget(self.budget_input)
        input_budget.add_widget(add_budget_button)
        self.layout.add_widget(input_budget)

        input_gasto_layout = BoxLayout(size_hint = (1, 0.2), spacing = 10, size_hint_y = 0.2, padding = (50,3,50,3))
        self.gasto_input = TextInput(hint_text = "Ingrese lo gastado", multiline = False, height = 150)
        add_gasto_button = Button(text = "Agrega gasto", on_press = self.sub_gasto, height = 150)
        input_gasto_layout.add_widget(self.gasto_input)
        input_gasto_layout.add_widget(add_gasto_button)
        self.layout.add_widget(input_gasto_layout) 

        self.budget_track_label = Label(text = "", font_size = '25sp', color = (0,0,0,1), halign = 'center', height = 30, size_hint_y = 0.3)
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
            self.budget_track_label.markup = True
            self.budget_track_label.text = f"[b]Error: Ingrese un numero valido[/b]"
            return 
        
    def sub_gasto(self, instance): 

        try: 
            gasto = float(self.gasto_input.text)
        except ValueError: 
            self.budget_track_label.markup = True
            self.budget_track_label.text = f"[b]Error: Ingrese un numero valido[/b]"
            return 

        if storage.exists("budget"): 
            budget = storage.get("budget")["total"]
        else: 
            budget = 0

        if gasto > budget: 
            self.budget_track_label.markup = True
            self.budget_track_label.text = f"[b]Se acabo tu presupuesto[/b]"
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
        self.budget_track_label.markup = True
        self.budget_track_label.text = f"[b]Presupuesto: ${budget:.2f}[/b]"

    def on_touch_move(self, touch):
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'inicio'


class Personas_Regalos_Main_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.layout = BoxLayout(orientation = 'vertical', padding = (10, 50,10,30), spacing = 10)

        instruction_label = Label (text = f"[b]Agrega a las personas[/b]", font_size = '30sp', color = (0,0,0,1), size_hint_y = 0.3, markup = True)
        self.layout.add_widget(instruction_label)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10, padding = (50,10,50,10))
        self.nombre_input = TextInput(hint_text = "Nombre de la persona", multiline = False, height = 140)
        add_person_button = Button(text = "Agregar persona", on_press = self.add_person, height = 140)
        input_area.add_widget(self.nombre_input)
        input_area.add_widget(add_person_button)
        self.layout.add_widget(input_area)

        self.layout.add_widget(Widget(size_hint_y = 0.2))

        self.scroll = ScrollView(size_hint = (1,0.8))
        self.lista_personas = BoxLayout(orientation = 'vertical', size_hint_y = None, spacing = 20)
        self.lista_personas.bind(minimum_height = self.lista_personas.setter('height'))
        self.scroll.add_widget(self.lista_personas)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)
    
        self.load_personas()

    def load_personas(self): 
        for persona in storage.keys(): 
            if persona in ["personas", "budget"]:
                continue 

            self.add_person_to_list(persona)

    def add_person_to_list(self, nombre): 
        persona_button = Button(text = nombre, pos_hint = {"center_x": 0.5}, size_hint = (0.92, None), height = 300, font_size = '20sp')
        persona_button.bind(on_press = lambda btn: self.open_person_screen(nombre))
        self.lista_personas.add_widget(persona_button)
    
    def add_person(self, instance):
        nombre = self.nombre_input.text.strip()
        if nombre:
            self.add_person_to_list(nombre)
            self.nombre_input.text = ""

    def open_person_screen(self, nombre):
        app = App.get_running_app()
        app.open_person_screen(nombre)
    
    def on_touch_move(self, touch): 
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'inicio'


class Editar_Personas(Screen):
    def __init__(self, persona_nombre, **kwargs): 
        super().__init__(**kwargs)

        self.persona_nombre = persona_nombre

        self.layout = BoxLayout(orientation = 'vertical', padding = (10, 20,10,10), spacing = 40)
        self.add_widget(self.layout)

        self.persona_label = Label(text = f"Regalos para {self.persona_nombre}", size_hint = (1, 0.1), font_size = "30sp", color = (0,0,0,1 ), size_hint_y = 0.2,font_name="Roboto-Bold.ttf")
        self.layout.add_widget(self.persona_label)

        regalo_pasado_layout = BoxLayout(size_hint = (1,0.2), spacing = 10, height = 80) #Falta ajusta el como se ve en la interfaz
        label_regalo_pasado = Label(text = "Te regalaron el año pasado?", size_hint = (5,1), font_size = '15sp', color = (0,0,0,1), halign = 'center')
        self.check_anio_pasado = CheckBox(size_hint_x = 3) 
        self.check_anio_pasado.bind(on_release=self.save_check_anio_pasado)
        regalo_pasado_layout.add_widget(label_regalo_pasado)
        regalo_pasado_layout.add_widget(self.check_anio_pasado)
        self.layout.add_widget(regalo_pasado_layout)

        barra_layout = BoxLayout( size_hint = (1, 0.2), spacing = 10, size_hint_y = 0.2, padding = (50,3,50,3))
        self.progrso_label = Label(text = "Progreso regalo", font_size = "20sp", color = (0,0,0,1), halign ="center")
        self.barra_progreso = ProgressBar(height = 200)
        barra_layout.add_widget(self.progrso_label)
        barra_layout.add_widget(self.barra_progreso)
        self.layout.add_widget(barra_layout)

        input_area = BoxLayout(size_hint = (1, 0.2), spacing = 10, size_hint_y = 0.2, padding = (50,10,50,10))
        self.regalo_input = TextInput(hint_text = "Ingresa regalo", multiline = False, height = 140)
        agreagar_button = Button(text = "Añadir", on_press = self.add_item, height = 140)
        input_area.add_widget(self.regalo_input)
        input_area.add_widget(agreagar_button)
        self.layout.add_widget(input_area)

        self.layout.add_widget(Widget(size_hint_y = 0.08))

        self.scroll = ScrollView(size_hint = (1, 0.8))
        self.checklist = BoxLayout(orientation = 'vertical', size_hint_y = None, spacing = 30, padding = (60,10,60,10))
        self.checklist.bind(minimum_height = self.checklist.setter("height"))
        self.scroll.add_widget(self.checklist)
        self.layout.add_widget(self.scroll)

        self.load_person_data()

    def load_person_data(self):
        if storage.exists(self.persona_nombre):
            data = storage.get(self.persona_nombre)
            regalos = data.get('regalos', [])
            self.barra_progreso.max = len(regalos)
            self.barra_progreso.value = sum(1 for regalo in regalos if regalo.get("marcado", False))
            self.check_anio_pasado.active = data.get('regalo_pasado', False)

            for regalo in regalos:
                gift_layout = self.create_gift_widget(regalo["nombre"], regalo.get("marcado", False))
                self.checklist.add_widget(gift_layout)

    def create_gift_widget(self, gift_text, marcado):
        gift_layout = BoxLayout(size_hint_y=None, height=80, spacing=30)

        checkbox = CheckBox(size_hint=(0.2, None), active=marcado, width = 60, height = 60)
        checkbox.bind(on_release=lambda cb: self.update_gift_status(gift_text, cb.active))

        regalo_label = Label(text=gift_text, size_hint=(0.5, 0.75), color=(0, 0, 0, 1), font_size = '20sp', height = '60sp', valign = 'middle', halign = 'center')
        delete_button = Button(text="Eliminar", size_hint=(0.3, None), width = 120, height = 60, font_size = '18sp')
        regalo_label.bind(size = regalo_label.setter('text_size'))
        delete_button.bind(on_press=lambda btn: self.remove_gift(gift_layout, gift_text))

        gift_layout.add_widget(checkbox)
        gift_layout.add_widget(regalo_label)
        gift_layout.add_widget(delete_button)
        return gift_layout
    
    def save_check_anio_pasado(self, instance): 
        if storage.exists(self.persona_nombre):
            data = storage.get(self.persona_nombre)
            data['regalo_pasado'] = self.check_anio_pasado.active
            storage.put(self.persona_nombre, **data)

    def update_gift_status(self, gift_text, marcado):
        if storage.exists(self.persona_nombre):
            data = storage.get(self.persona_nombre)
            regalos = data.get('regalos', [])
            for regalo in regalos:
                if regalo["nombre"] == gift_text:
                    regalo["marcado"] = marcado
                    break
            
            storage.put(self.persona_nombre, regalos = regalos)
            self.barra_progreso.value = sum(1 for regalo in regalos if regalo.get("marcado", False))

    def add_item(self, instance):
        gift_text = self.regalo_input.text.strip()

        if gift_text:
            gift_layout = self.create_gift_widget(gift_text, False)
            self.checklist.add_widget(gift_layout)

            if not storage.exists(self.persona_nombre):
                storage.put(self.persona_nombre, regalos=[])
            data = storage.get(self.persona_nombre)
            regalos = data.get('regalos', [])
            regalos.append({"nombre": gift_text, "marcado": False})
            storage.put(self.persona_nombre, regalos = regalos)

            self.barra_progreso.max = len(regalos)
            self.regalo_input.text = ""

    def remove_gift(self, item_layout, gift_text):
        self.checklist.remove_widget(item_layout)
        
        if storage.exists(self.persona_nombre):
            data = storage.get(self.persona_nombre)
            regalos = data.get('regalos', [])
            regalos = [regalo for regalo in regalos if regalo["nombre"] != gift_text]
            storage.put(self.persona_nombre, regalos = regalos)

            self.barra_progreso.max = len(regalos)
            self.barra_progreso.value = sum(1 for regalo in regalos if regalo.get("marcado", False)) 
    
    def on_touch_move(self, touch): 
        app = App.get_running_app() 
        app.root.transition = SlideTransition(direction = "right")
        if touch.dx > 50: 
            self.manager.current = 'AddPerson'

    def on_pre_leave(self): 
        if platform == 'android':
            app = App.get_running_app() 
            app.root.transition = SlideTransition(direction = "right")
            app.root.current = 'AddPerson'


class Lista_Regalos(App):
    def build(self):
        
        self.sm = ScreenManager()
        self.sm.add_widget(Pantalla_Inicio(name = 'inicio'))
        self.sm.add_widget(Pantalla_Presupuesto(name = 'presupuesto'))
        self.sm.add_widget(Personas_Regalos_Main_Screen(name = 'AddPerson'))

        if platform == 'android': 
            EventLoop.window.bind(on_keyboard = self.android_back_button)

        return self.sm
    
    def open_person_screen(self, nombre):
        screen_name = f'person_screen_{nombre}'
        if screen_name not in [screen.name for screen in self.sm.screens]:

            new_screen = Editar_Personas(name = screen_name, persona_nombre = nombre)
            self.sm.add_widget(new_screen)

        self.sm.transition = SlideTransition(direction = "left")
        self.sm.current = screen_name

    def android_back_button(self, window, key, *args): 
        if key == 27: 
            screen_manager = self.root
            if screen_manager.current != 'inicio': 
                app = App.get_running_app() 
                app.root.transition = SlideTransition(direction = "right")
                screen_manager.current = 'inicio'
                return True
            return False

    def on_stop(self):
        return super().on_stop()


Lista_Regalos().run()