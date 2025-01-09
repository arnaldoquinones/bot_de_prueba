import reflex as rx
from rxconfig import config
import re  # Para usar expresiones regulares en la validación del email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import requests


# -------------------------
# -- BARRA SIDEBAR  MENU --
# -------------------------



class SidebarState(rx.State):
    is_open: bool = False

    def on_mount(self):
        """Initialize sidebar as closed when component mounts"""
        self.is_open = False

    @rx.event
    def toggle_sidebar(self):
        self.is_open = not self.is_open  # Alterna entre abierto y cerrado


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
        create_sidebar_item("Chatbot", "bot-message-square"),
        create_sidebar_item("Messages", "mail", on_click=None),  # Asegúrate de definir la función de click si la necesitas
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
        shadow="md",
    )



def sidebar_with_toggle() -> rx.Component:
    """Permite alternar la visibilidad del sidebar."""
    return rx.box(
        rx.icon(
            "menu",
            on_click=SidebarState.toggle_sidebar,
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



def header():
    """Encabezado personalizado para el sitio web."""
    return rx.box(
        # Caja contenedora general
        rx.flex(
            sidebar_with_toggle(),
            # rx.box(
            #     rx.icon("menu", size=40, margin_top="0.8em", margin_left="2em", on_click=SidebarState.toggle_sidebar),  # Llamar al toggle
            #     align="start",
            #     flex="none",
            # ),
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
        rx.box(
            rx.text(
            """ "...Scientia est potentia..." """,
            font_size="1.5em",
            font_style="italic", 
            text_align="right",
            color="white",
            margin_top="3em",
            margin_right="2em",
            style=style["animate"]  # Apply style directly
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
                                "min_width": "270px"
                            },
                        ),
                        rx.input(
                            placeholder="Last Name",
                            name="last_name",
                            required=True,
                            style={
                                "text-align": "left",
                                "min_width": "270px"
                            },
                        ),
                        rx.cond(
                            MessageFormStateV2.email_error,  # Si hay error
                            rx.input(
                                placeholder=MessageFormStateV2.email_error,
                                name="email",
                                required=True,
                                style={"border": "1px solid red",
                                       "min_width": "270px"},
                            ),
                            rx.input(
                                placeholder="Email",
                                name="email",
                                required=True,
                                style={"border": "1px solid gray",
                                       "min_width": "270px"},
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
                        rx.hstack(
                            rx.button(
                                "Submit", 
                                type="submit",
                                is_loading=MessageFormStateV2.is_submitting,
                            ),
                            rx.cond(
                                MessageFormStateV2.submit_status == "success",
                                rx.text(
                                    "Message sent successfully!",
                                    color="green",
                                    font_size="sm",
                                ),
                            ),
                            rx.cond(
                                MessageFormStateV2.submit_status == "error",
                                rx.text(
                                    "Something went wrong, try later.",
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
                # "max-height": "350px"
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
class WeatherState(rx.State):
    """The app state."""
    location: str = ""
    temperature: float = 0
    weather_desc: str = ""
    loading: bool = False

    def get_weather(self):
        """Get weather data for the location."""
        if self.location == "":
            return rx.window_alert("Please enter a location")
        
        self.loading = True
        yield
        
        # Replace with your API key and actual API call
        API_KEY = "your_api_key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()
            self.temperature = data["main"]["temp"]
            self.weather_desc = data["weather"][0]["description"]
        except:
            return rx.window_alert("Error fetching weather data")
        finally:
            self.loading = False

def index():
    return rx.vstack(
        rx.heading("Weather App"),
        rx.input(
            placeholder="Enter location",
            on_blur=WeatherState.set_location,
        ),
        rx.button(
            "Get Weather",
            on_click=WeatherState.get_weather,
        ),
        rx.cond(
            WeatherState.loading,
            rx.spinner(),
            rx.vstack(
                rx.heading(f"Temperature: {WeatherState.temperature}°C"),
                rx.text(f"Weather: {WeatherState.weather_desc}"),
            ),
        ),
    )

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
