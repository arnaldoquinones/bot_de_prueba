import reflex as rx
from rxconfig import config
import re  # Para usar expresiones regulares en la validación del email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import requests
import time
import asyncio
import datetime as dt
import locale

# -------------------------
# -- BARRA SIDEBAR  MENU --
# -------------------------

class SidebarState(rx.State):
    is_open: bool = False
    last_activity: float = time.time()  # Tiempo de la última actividad

    # Estado para controlar si la ventana del chatbot está abierta o cerrada
    chatbot_window_open: bool = False  # Aquí controlamos si la ventana está abierta o cerrada

    def on_mount(self):
        """Inicializa el estado cuando el componente se monta"""
        self.is_open = False
        self.last_activity = time.time()  # Establecer la última actividad al momento de montar

    @rx.event
    def toggle_sidebar(self):
        """Alterna entre abrir y cerrar el sidebar"""
        self.is_open = not self.is_open
        self.last_activity = time.time()  # Resetea el temporizador al interactuar

    @rx.event
    def open_chat_window(self):
        """Acción para abrir la ventana del chatbot"""
        self.chatbot_window_open = True  # Establecer el estado como abierto

    @rx.event
    def reset_last_activity(self):
        """Actualizar el tiempo de la última actividad al interactuar"""
        self.last_activity = time.time()
        print("Actividad detectada. Última actividad actualizada.")  # Para fines de depuración


def create_sidebar_item(text: str, icon: str, href: str = None, on_click: rx.EventHandler = None) -> rx.Component:
    """Crea un único elemento del menú lateral."""
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
    """Crea la lista completa de elementos del menú lateral."""
    return rx.vstack(
        rx.flex(
            rx.input(
                rx.input.slot(
                    rx.icon(tag="search"),
                ),
                placeholder="Ingrese consulta",
            ),
            direction="column",
            spacing="3",
            style={"maxWidth": 500},
        ),
        create_sidebar_item("About me", "user", href="./about"),
        create_sidebar_item("Projects", "square-library", href="./proyects"),
        create_sidebar_item("Skills", "bar-chart-4", href="./skills"),
        create_sidebar_item("Chatbot", "bot-message-square", on_click=SidebarState.open_chat_window),  # Acción para abrir el chat
        create_sidebar_item("Messages", "mail", on_click=MessageFormStateV2.toggle_popover),  # Asegúrate de definir la función de click si la necesitas
        spacing="2",
        width="12em",
    )


def sidebar_bottom_profile() -> rx.Component:
    """Define el perfil inferior del sidebar con transición fluida."""
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
            transition="transform 0.3s ease-in-out",  # Control de deslizamiento
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
    """Script para inicializar el efecto de sonido."""
    return rx.script(
        """
        var button_sfx = new Audio("https://github.com/arnaldoquinones/bot_de_prueba/raw/refs/heads/master/src/pages/assets/mouse-click-sound-trimmed.mp3");
        function playFromStart(sfx) {sfx.load(); sfx.play();}
        """
    )


def sidebar_with_toggle() -> rx.Component:
    """Permite alternar la visibilidad del sidebar con efecto de sonido."""
    return rx.box(
        sound_effect_script(),  # Agregar el script de sonido
            rx.icon(
                "menu",
                # Combinar el efecto de sonido y el cambio de estado
                on_click=[
                    rx.call_script("playFromStart(button_sfx)"),
                    SidebarState.toggle_sidebar,  # Acción de alternar el sidebar
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
    sender_email = "arnaldpqportfolio@gmail.com"  # Cambia esto a tu correo
    receiver_email = "arnaldpqportfolio@gmail.com"  # Correo que recibirá los mensajes
    sender_password = "xxx"  # Contraseña del remitente

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
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Usando SMTP de Gmail
            server.starttls()  # Inicia conexión segura
            server.login(sender_email, sender_password)  # Inicia sesión
            server.send_message(msg)  # Envía el correo
            print("Correo enviado exitosamente.")
            return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

class MessageFormStateV2(rx.State):
    is_popover_open: bool = False  # Controla la visibilidad del pop-up
    form_data: dict = {}          # Almacena los datos enviados del formulario
    email_error: str = ""         # Mensaje de error en el campo de email
    submit_status: str = ""       # Para rastrear el estado del envío
    is_submitting: bool = False   # Para controlar el estado durante el envío

    @rx.event
    def toggle_popover(self):
        """Alterna la visibilidad del pop-up."""
        self.is_popover_open = not self.is_popover_open
        self.submit_status = ""  # Resetear el estado del envío al abrir/cerrar

    @rx.event
    def validate_email(self, email: str) -> bool:
        """Valida el formato del email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @rx.event
    async def handle_submit(self, form_data: dict):
        """Maneja el envío del formulario."""
        print("Formulario recibido:", form_data)
        email = form_data.get("email", "").strip()

        if not self.validate_email(email):
            self.email_error = "Please enter a valid email address."
            return

        self.email_error = ""
        self.form_data = form_data
        self.is_submitting = True

        # Intentar enviar el email
        if send_email(form_data):
            self.submit_status = "success"
            await rx.sleep(2)  # Esperar 2 segundos antes de cerrar
            self.is_popover_open = False
        else:
            self.submit_status = "error"
        
        self.is_submitting = False

def pop_up_message():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.heading("Contact me", size="4", color="white"),
                rx.dialog.close(
                    rx.button(
                        rx.icon("x"),
                        size="1",
                        on_click=MessageFormStateV2.toggle_popover,
                        style={
                            "position": "absolute",
                            "top": "0",
                            "right": "0",
                            "background": "transparent",
                            "border": "transparent",
                            "color": "white",
                            "padding": "0",
                            "font-size": "1px",
                        },
                    )
                ),
            ),
            rx.dialog(
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="First Name",
                            name="first_name",
                            required=True,
                            style={
                                "text-align": "left",
                                "min_width": "270px",
                            },
                        ),
                        rx.input(
                            placeholder="Last Name",
                            name="last_name",
                            required=True,
                            style={
                                "text-align": "left",
                                "min_width": "270px",
                            },
                        ),
                        rx.cond(
                            MessageFormStateV2.email_error,
                            rx.input(
                                placeholder=MessageFormStateV2.email_error,
                                name="email",
                                required=True,
                                style={
                                    "border": "1px solid red",
                                    "min_width": "270px",
                                },
                            ),
                            rx.input(
                                placeholder="Email",
                                name="email",
                                required=True,
                                style={
                                    "border": "1px solid gray",
                                    "min_width": "270px",
                                },
                            ),
                        ),
                        rx.text_area(
                            placeholder="Write your message",
                            name="message",
                            required=True,
                            style={
                                "text-align": "left",
                                "resize": "vertical",
                                "overflow": "auto",
                                "min_height": "130px",
                                "max_height": "270px",
                                "min_width": "270px",
                                "white-space": "pre-wrap",
                                "word-wrap": "break-word",
                            },
                        ),
                        rx.hstack(sound_effect_script(),
                            rx.button(
                                "Submit",
                                type="submit",
                                is_loading=MessageFormStateV2.is_submitting,
                                border="none",
                                border_radius="10px",
                                color="white",
                                # box_shadow="0 0 25px #1e88e5, 0 0 15px #1e88e5 inset, 0 8px 0 #1565c0",
                                transform="perspective(1px) translateZ(0)",
                                transition="all .3s ease",
                                # Text shadow for extra depth
                                # text_shadow="2px 2px 4px rgba(0,0,0,0.3)",
                                # Hover state
                                # _hover={
                                #     "transform": "scale(1.05) translateY(-2px)",
                                #     "box_shadow": "0 0 35px #1e88e5, 0 0 20px #1e88e5 inset, 0 10px 0 #1565c0",
                                # },
                                # Active/Click state
                                _active={
                                    "transform": "scale(0.95) translateY(4px)",
                                    "box_shadow": "0 0 15px #0E1CFF, 0 0 10px #0E1CFF inset, 0 4px 0 #1565c0",
                                },
                                on_click=[
                                rx.call_script("playFromStart(button_sfx)"),  # Agrega el efecto de sonido
                            ]
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
                                    "🤦Something went wrong! Try again later.",
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

# ------ FIN DE POP UP WINDOW MAIL ------



# --------------------------
# -- WEATHER LOCATION API --
# --------------------------

import os
import reflex as rx  # Reflex es el framework
import requests
from dotenv import load_dotenv

# load_dotenv()

# # Clave de la API
# API_KEY = os.getenv("api_weather_key")
import reflex as rx
import requests

# Configuración de la API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "cc927a091110908fb4a1fe8ac93353b1"  # Coloca tu API Key aquí
CITY = "Buenos Aires"  # No lo mostramos, pero lo usamos para la API

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
