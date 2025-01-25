import reflex as rx
from rxconfig import config
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .bot_interface import State
from dotenv import load_dotenv
import os
import requests
import time
import asyncio
import datetime as dt
import locale
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser

# --------------------
# --- SIDEBAR MENU ---
# --------------------

# Crear esquema y índice
def create_whoosh_index():
    # Paso 1: Crear el esquema de Whoosh
    schema = Schema(content=TEXT(stored=True))

    # Paso 2: Crear índice en la carpeta 'index'
    if not os.path.exists("index"):
        os.mkdir("index")
    index_dir = "index"
    ix = create_in(index_dir, schema)

    return ix

ix = create_whoosh_index()


class SidebarState(rx.State):
    is_open: bool = False
    last_activity: float = time.time()
    chatbot_window_open: bool = False
    auto_hide_time: float = 10
    search_query: str = ""  # Puedes asignar un valor por defecto si lo deseas

    @rx.event
    def set_search_query(self, query: str):
        """Establece la consulta de búsqueda."""
        self.search_query = query  # Ahora esta variable está definida y puedes usarla

    def on_mount(self):
        self.is_open = False

    @rx.event
    def set_search_query(self, query: str):
        """Establece el término de búsqueda y redirige a la página resumen."""
        self.search_query = query
        # Realiza la búsqueda en Whoosh
        self.perform_search(query)
        return rx.redirect("/resumen")  # Redirigir a la página de resultados

    def perform_search(self, query: str):
        """Realiza la búsqueda en el índice de Whoosh."""
        with ix.searcher() as searcher:
            query_parser = QueryParser("content", ix.schema)
            query_obj = query_parser.parse(query)
            results = searcher.search(query_obj)
            for result in results:
                print(f"Found: {result['content']}")  # Muestra los resultados encontrados


    @rx.event
    def toggle_sidebar(self):
        self.is_open = not self.is_open
        if self.is_open:
            return SidebarState.start_auto_hide_timer

    @rx.event(background=True)
    async def start_auto_hide_timer(self):
        await asyncio.sleep(self.auto_hide_time)
        async with self:
            self.is_open = False


    @rx.event
    def toggle_window(self):
        self.chatbot_window_open = not self.chatbot_window_open
        print(f"Ventana del chatbot {'abierta' if self.chatbot_window_open else 'cerrada'}")

    @rx.event
    def open_chat_window(self):
        self.chatbot_window_open = True

    @rx.event
    def reset_last_activity(self):
        self.last_activity = time.time()
        print("Actividad detectada. Última actividad actualizada.")

def create_sidebar_item(text: str, icon: str, href: str = None, on_click: rx.EventHandler = None) -> rx.Component:
    link_props = {"href": href} if href else {"on_click": on_click}
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                    "box-shadow": "0px 10px 20px rgba(0, 0, 0, 0.8)",
                },
                "border-radius": "0.5em",
            },
        ),
        **link_props,
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_item() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon(tag="search", size=16), style={"order": 1}),
                placeholder="Ingrese consulta",
                max_length=50,
                border_radius="90px",
                style={"text_align": "center"},
                on_change=SidebarState.set_search_query,  # Capturar la consulta
            ),
            direction="column",
            spacing="3",
            style={"maxWidth": 500},
        ),
        create_sidebar_item("About me", "user", href="./about"),
        create_sidebar_item("Projects", "square-library", href="./proyects"),
        create_sidebar_item("Skills", "bar-chart-4", href="./skills"),
        create_sidebar_item("Chatbot", "bot-message-square", on_click=State.toggle_window),
        create_sidebar_item("Messages", "mail", on_click=MessageFormStateV2.toggle_popover),
        spacing="2",
        width="12em",
    )

def sidebar_bottom_profile() -> rx.Component:
    return rx.box(
        rx.vstack(
            sidebar_item(),
            rx.divider(margin_y="2em"),
            rx.hstack(
                rx.text("Made by", size="3", weight="bold"),
                rx.link(
                    "A. Quiñones",
                    href="https://github.com/arnaldoquinones",
                    size="3",
                    weight="medium",
                    color="blue.500",
                    is_external=True,
                ),
                padding_x="0.5rem",
                align="center",
                justify="start",
                width="100%",
                margin_top="-0.7cm",
            ),
            spacing="2",
            margin_top="auto",
            padding_x="1em",
            padding_y="0.5cm",
            bg=rx.color("accent", 3),
            align="start",
            height="calc(100vh - 60px)",
            overflow="auto",
            width="14em",
            position="fixed",
            left="0",
            top="160px",
            transform=rx.cond(SidebarState.is_open, "translateX(0)", "translateX(-100%)"),
            transition="transform 0.3s ease-in-out",
        ),
        bg=rx.color("accent", 2),
        shadow="xl",
    )


class SoundEffectState(rx.State):
    @rx.event(background=True)
    async def delayed_play(self):
        await asyncio.sleep(1)
        return rx.call_script("playFromStart(button_sfx)")

def sound_effect_script():
    return rx.script(
        """
        var button_sfx = new Audio("https://github.com/arnaldoquinones/bot_de_prueba/raw/refs/heads/master/src/pages/assets/mouse-click-sound-trimmed.mp3");
        function playFromStart(sfx) {sfx.load(); sfx.play();}
        """
    )

def sidebar_with_toggle() -> rx.Component:
    return rx.box(
        sound_effect_script(),
        rx.cond(
            SidebarState.is_open,
            rx.icon(
                "arrow-left",
                on_click=[
                    rx.call_script("playFromStart(button_sfx)"),
                    SidebarState.toggle_sidebar,
                ],
                position="absolute",
                left="7%",
                top="13%",
                transform="translate(-50%, -50%)",
                color_scheme="teal",
                background="transparent",
                size=48,
                cursor="pointer",
            ),
            rx.icon(
                "menu",
                on_click=[
                    rx.call_script("playFromStart(button_sfx)"),
                    SidebarState.toggle_sidebar,
                ],
                position="absolute",
                left="7%",
                top="13%",
                transform="translate(-50%, -50%)",
                color_scheme="teal",
                background="transparent",
                size=48,
                cursor="pointer",
            )
        ),
        sidebar_bottom_profile(),
    )


# ------ FIN DE LA BARRA SIDEBAR MENU ------





# --------------
# --- HEADER ---
# --------------

style = {
    "animate": {
        "opacity": "0",
        "animation": "fadeIn 4s ease-in-out forwards",
        "@keyframes fadeIn": {
            "from": {"opacity": "0"},
            "to": {"opacity": "1"}
        }
    }
}
import requests
from datetime import datetime
import locale

def get_date_and_location():
    """Obtiene la fecha actual y la ubicación según la IP."""
    try:
        # Configurar el locale a español (Argentina)
        locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')

        # Obtener la fecha sin la coma
        current_date = datetime.now().strftime("%A %d %B")

        # Separar los componentes
        day_of_week, day, month = current_date.split()
        
        # Capitalizar el día de la semana y el mes
        day_of_week = day_of_week.capitalize()
        month = month.capitalize()
        
        # Reconstruir la fecha con "de"
        current_date = f"{day_of_week} {day} de {month}"

        # Obtener la ubicación basada en la IP
        location_response = requests.get("https://ipinfo.io?token=413cc4ca42c4bd")
        if location_response.status_code == 200:
            location_data = location_response.json()
            city = location_data.get("city", "Unknown City")
            location = city
        else:
            location = "Location unavailable"
    except Exception as e:
        current_date = "Date unavailable"
        location = f"Error: {e}"
    
    return current_date, location


def header():
    """Encabezado personalizado para el sitio web, incluyendo clima."""
    # Obtener la fecha y ubicación
    current_date, location = get_date_and_location()
    
    return rx.box(
        # Caja contenedora general
        rx.flex(
            sidebar_with_toggle(),
            rx.flex(
                rx.link(
                    rx.heading(
                        "My Portfolio",
                        style={
                            "text_shadow": "8px 8px 16px rgba(0, 0, 0, 1)",
                        },
                        size="9",
                        color="white",
                    ),
                    href="/",
                    is_external=False,
                    on_click=rx.call_script("playFromStart(button_sfx)"),  # Agrega el sonido al clic
                ),
                gap="2",
                align="center",
                justify="center",
                flex="1",
                direction="column",
            ),
            gap="2",
            align_items="center",
            width="100%",
            justify_content="flex-start",
            flex_direction="row",
        ),
        # Caja para fecha y ubicación
        rx.box(
            rx.text(
                f"{current_date} - {location}",
                font_size="1em",
                color="white",
                margin_top="5em",
                margin_right="58em",
                text_align="right",
            ),
            position="absolute",
            top="0",
            right="0",
        ),
        # Caja para el clima
        rx.box(
            rx.flex(
            rx.heading(f"{temperature}°C  ", size="3", color="white"),
            rx.text(f"{description}", size="3", color="white"),
            align="center",
            direction="row",  # Cambiado de 'column' a 'row'
            gap="1rem",
            padding="1rem",
        ),
            position="absolute",
            top="-2px",
            left="130px",
            margin_top="3em",
            margin_left="2em",
        ),
        # Caja para la cita
        rx.box(
            rx.text(
                """ "...Scientia est potentia..." """,
                font_size="1.5em",
                font_style="italic", 
                text_align="right",
                color="white",
                margin_top="3em",
                margin_right="2em",
                style=style["animate"]
            ),
            position="absolute",
            top="0",
            right="0",
        ),
        background_image="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/banner_header.jpg?raw=true')",
        background_size="cover",
        width="100%",
        height="160px",
        display="flex",
        justify_content="center",
        align_items="center",
        box_shadow="0px 10px 20px rgba(0, 0, 0, 0.7), 0px 0px 10px transparent",
    )



# ------ FIN DE HEADER ------


# -------------------------
# -- POP UP WINDOW EMAIL --
# -------------------------
class MessageFormState(rx.State):
    form_data: dict = {}
    is_popover_open: bool = False  # Estado para controlar la visibilidad del pop-up

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        self.is_popover_open = False  # Cierra el pop-up después de enviar el formulario

    @rx.event
    def toggle_popover(self):
        """Toggle the popover visibility."""
        self.is_popover_open = not self.is_popover_open


load_dotenv()

def send_email(form_data: dict):
    """
    Envía un correo electrónico utilizando los datos del formulario.
    """
    sender_email = "arnaldopqportfolio@gmail.com"
    receiver_email = "arnaldopqportfolio@gmail.com"
    sender_password = os.getenv('email_pass')

    # Crear el contenido del correo
    subject = "Nuevo mensaje de contacto desde tu sitio web"
    body = f"""
    Has recibido un nuevo mensaje de contacto:

    Nombre: {form_data.get('first_name')} {form_data.get('last_name')}
    Email: {form_data.get('email')}
    Mensaje:
    {form_data.get('message')}
    """

    # Configurar el mensaje
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Enviar el correo
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Correo enviado exitosamente.")
            return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

# class MessageFormStateV2(rx.State):
class MessageFormStateV2(rx.State):
    is_popover_open: bool = False
    form_data: dict = {}
    email_error: str = ""
    name_error: str = ""  # Variable para el error del nombre
    submit_status: str = ""
    is_submitting: bool = False

    def set_form_data(self, field_name: str, value: str):
        """Actualiza los datos del formulario."""
        self.form_data[field_name] = value

    def validate_name(self):
        """Valida que el campo nombre no esté vacío y actualiza el estado."""
        if not self.form_data.get("first_name", "").strip():
            self.name_error = "This field is required."
        else:
            self.name_error = ""

    def validate_email(self, email: str) -> bool:
        """Valida el formato del email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @rx.event
    def toggle_popover(self):
        """Alterna la visibilidad del pop-up."""
        self.is_popover_open = not self.is_popover_open

    @rx.event 
    async def handle_submit(self, form_data: dict):
        """Maneja el envío del formulario."""
        # Validar nombre
        self.validate_name()
        if self.name_error:
            return

        # Validar email
        email = form_data.get("email", "").strip()
        if not self.validate_email(email):
            self.email_error = "Please enter a valid email address."
            return
        
        # Resetear errores y activar 'enviando'
        self.email_error = ""
        self.is_submitting = True
        yield  # Fuerza la UI a mostrar "Sending..."

        # Simular envío de email
        await asyncio.sleep(1)  # Simulación opcional
        success = send_email(form_data)  # <-- Reemplaza con tu lógica
        
        # Manejar resultado
        if success:
            self.submit_status = "success"
            yield rx.toast("😎 Message sent!", duration=2000)
        else:
            self.submit_status = "error"
            yield rx.toast("🤦 Error!", duration=2000)

        # Ocultar "Sending..." inmediatamente
        self.is_submitting = False
        yield  # Actualización UI

        # Esperar 2s y cerrar pop-up
        await asyncio.sleep(2)
        self.submit_status = ""
        self.is_popover_open = False


# Animación de parpadeo
blink_animation = {
    "animation": "blink 1s infinite",
    "@keyframes blink": {
        "0%": {"opacity": 1},
        "50%": {"opacity": 0},
        "100%": {"opacity": 1},
    },
}
        

def pop_up_message():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.image(
                        src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                        width="30px",
                        height="auto",
                        style={
                            "position": "absolute",
                            "left": "15px",
                            "top": "6%",
                            "transform": "translateY(-50%)",
                        },
                    ),
                    rx.heading(
                        "Contact me",
                        size="4",
                        color="white",
                        align="center",
                    ),
                    spacing="3",
                    align_items="center",
                    justify_content="center",
                    width="100%",
                ),
            ),
            rx.dialog.close(
                rx.button(
                    rx.icon("x"),
                    size="1",
                    on_click=MessageFormStateV2.toggle_popover,
                    style={
                        "position": "absolute",
                        "top": "6px",
                        "right": "6px",
                        "background": "transparent",
                        "border": "transparent",
                        "color": "white",
                        "padding": "0",
                        "font-size": "1px",
                    },
                )
            ),
            rx.dialog(
                rx.form(
                    rx.vstack(
                        # Input para First Name con validación
                        rx.vstack(
                            rx.input(
                                placeholder="First Name",
                                name="first_name",
                                required=True,
                                max_length=50,
                                on_change=lambda value: MessageFormStateV2.set_form_data("first_name", value),
                                on_blur=lambda _: MessageFormStateV2.validate_name(),
                                style={
                                    "border": rx.cond(
                                        MessageFormStateV2.name_error != "",
                                        "1px solid red",
                                        "1px solid gray",
                                    ),
                                    "min-width": "270px",
                                },
                            ),
                            rx.cond(
                                MessageFormStateV2.name_error != "",
                                rx.text(
                                    MessageFormStateV2.name_error,
                                    color="red",
                                    font_size="sm",
                                ),
                            ),
                        ),
                        # Input para Last Name (opcional, sin validación adicional)
                        rx.input(
                            placeholder="Last Name",
                            name="last_name",
                            required=False,
                            max_length=50,
                            style={
                                "text-align": "left",
                                "min-width": "270px",
                                "border": "1px solid gray",
                            },
                        ),
                        # Input para Email con validación
                        rx.vstack(
                            rx.input(
                                placeholder="Email",
                                name="email",
                                required=True,
                                max_length=500,
                                style={
                                    "border": rx.cond(
                                        MessageFormStateV2.email_error != "",
                                        "1px solid red",
                                        "1px solid gray",
                                    ),
                                    "min-width": "270px",
                                },
                            ),
                            rx.cond(
                                MessageFormStateV2.email_error != "",
                                rx.text(
                                    MessageFormStateV2.email_error,
                                    color="red",
                                    font_size="sm",
                                ),
                            ),
                        ),
                        # Text Area para el mensaje
                        rx.text_area(
                            placeholder="Write your message",
                            name="message",
                            required=True,
                            style={
                                "text-align": "left",
                                "resize": "vertical",
                                "overflow": "auto",
                                "min-height": "130px",
                                "max-height": "270px",
                                "min-width": "270px",
                                "white-space": "pre-wrap",
                                "word-wrap": "break-word",
                            },
                        ),
                        # Botón Submit y mensajes de estado
                        rx.hstack(
                            rx.button(
                                "Submit",
                                type="submit",
                                is_loading=MessageFormStateV2.is_submitting,
                                loading_text="Sending...",
                                border="none",
                                border_radius="10px",
                                color="white",
                                transform="perspective(1px) translateZ(0)",
                                transition="all .3s ease",
                                _active={
                                    "transform": "scale(0.95) translateY(4px)",
                                    "box_shadow": "0 0 15px #0E1CFF, 0 0 10px #0E1CFF inset, 0 4px 0 #1565c0",
                                },
                            ),
                            rx.cond(
                                MessageFormStateV2.is_submitting,
                                rx.text(
                                    "📤 Sending...",
                                    color="blue",
                                    font_size="sm",
                                    style=blink_animation,
                                ),
                            ),
                            rx.cond(
                                MessageFormStateV2.submit_status == "success",
                                rx.text(
                                    "😎 Message sent successfully!",
                                    color="green",
                                    font_size="sm",
                                ),
                            ),
                            rx.cond(
                                MessageFormStateV2.submit_status == "error",
                                rx.text(
                                    "🤦 Something went wrong! Try again later.",
                                    color="red",
                                    font_size="13px",
                                ),
                            ),
                            align_items="center",
                            spacing="3",
                        ),
                    ),
                    on_submit=MessageFormStateV2.handle_submit,
                    reset_on_submit=True,
                ),
            ),
            style={
                "max-width": "300px",
                "width": "auto",
                "min-height": "250px",
                "padding": "1rem",
                "position": "relative",
                "background": rx.color("accent", 3),
            },
        ),
        open=MessageFormStateV2.is_popover_open,
    )














# --------------------------
# -- WEATHER LOCATION API --
# --------------------------

import os
import reflex as rx  # Reflex es el framework
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API
BASE_URL = os.getenv('BASE_URL')

load_dotenv()
API_KEY = os.getenv('api_wether_key') 
CITY = "Buenos Aires" 

# Función para convertir Kelvin a Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Obtener los datos del clima
def fetch_weather():
    url = f"{BASE_URL}?q={CITY}&appid={API_KEY}"
    response = requests.get(url).json()
    temp_kelvin = response["main"]["temp"]
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    description = response["weather"][0]["description"]
    return round(temp_celsius, 2), description.capitalize()

# Obtener datos directamente
temperature, description = fetch_weather()


def index():
    pass

    app = rx.App()
    app.add_page(index)





# -- CODIGO DE MODULOS -- 
# rx.stack(
            #             rx.container(
            #                 width="200px",
            #                 height="45vh",
            #                 center_content=True,
            #                 bg=rx.color("accent", 3),
            #                 border_radius="15px",
            #                 box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
            #             ),
            #             position="absolute",  # Posicionamiento absoluto
            #             bottom="2%",  # Alineado al borde inferior
            #             right="60%",  # Alineado al borde izquierdo
            #         ),



