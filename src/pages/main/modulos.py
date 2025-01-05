import reflex as rx
from rxconfig import config
import re  # Para usar expresiones regulares en la validación del email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------------
# -- BARRA SIDEBAR  MENU --
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



def sidebar_item(text: str, icon: str, href: str = None, on_click: rx.EventHandler = None) -> rx.Component:
    """Crea un elemento del menú lateral."""
    link_props = {"href": href} if href else {"on_click": on_click}

    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="90%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        **link_props,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("About me", "user", href="./about"),
        sidebar_item("Projects", "square-library", href="./proyects"),
        sidebar_item("Skills", "bar-chart-4", href="./skills"),
        sidebar_item("Languages", "languages", href="./skills"),
        sidebar_item("Chatbot", "bot-message-square", href="./skills"),
        sidebar_item("Messages", "mail", on_click=MessageFormStateV2.toggle_popover),  # Alterna el pop-up
        spacing="3",
        width="12em",
    )


def sidebar_bottom_profile() -> rx.Component:
    """Crea el perfil inferior de la barra lateral."""
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="/logo.png",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        href="./",  # Ruta a la página principal (main)
                    ),
                    rx.link(
                        rx.heading(
                            "My portfolio.", size="5", weight="bold"
                        ),
                        href="./",  # Ruta a la página principal (main)
                        style={
                            "color": "white",  # Mantiene el color del texto en blanco
                            "text-decoration": "none",  # Elimina subrayados
                            "_hover": {
                                "color": "white",  # Mantiene blanco al pasar el mouse
                            },
                        },
                    ),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                # Aquí mueve el divider dentro del contenedor flexible
                rx.vstack(
                    rx.divider(margin_y="2"),  # Divider ahora está dentro del vstack
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.text(
                                    "Made by",
                                    size="3",
                                    weight="bold",
                                ),
                                rx.link(
                                    "Arnaldo Quiñones",
                                    href="https://github.com/arnaldoquinones",
                                    size="2",
                                    weight="medium",
                                    color="blue.500",
                                    is_external=True,
                                ),
                                width="100%",
                            ),
                            align="start",
                            justify="start",
                            width="100%",
                        ),
                        padding_x="0.5rem",
                        align="center",
                        justify="start",
                        width="100%",
                    ),
                    width="100%",
                    spacing="2",  # Espaciado entre elementos inferiores
                    margin_top="auto",  # Empuja este contenido al fondo
                ),
                spacing="3",  # Espaciado general ajustado
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",  # Ajusta la altura para que ocupe todo el alto de la página
                width="12em",  # Mantén el ancho fijo si lo deseas
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.icon("align-justify", size=30)
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    rx.icon("x", size=30)
                                ),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.vstack(
                                rx.divider(margin_y="2"),  # Divider en la versión móvil también
                                rx.hstack(
                                    rx.icon_button(
                                        rx.icon("user"),
                                        size="3",
                                        radius="full",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.text(
                                                "Made by",
                                                size="3",
                                                weight="bold",
                                            ),
                                            rx.link(
                                                "Arnaldo Quiñones",
                                                href="https://github.com/arnaldoquinones",
                                                size="2",
                                                weight="medium",
                                                color="blue.500",
                                                is_external=True,
                                            ),
                                            width="100%",
                                        ),
                                        justify="start",
                                        width="100%",
                                    ),
                                    padding_x="0.5rem",
                                    align="center",
                                    justify="start",
                                    width="100%",
                                ),
                                spacing="2",  # Espaciado entre los elementos inferiores
                                width="100%",
                            ),
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",  # Ajusta el contenido a la altura completa de la pantalla
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )

# -------------------------
# -- POP UP WINDOW EMAIL --
# -------------------------
import reflex as rx
from rxconfig import config
import re  # Para usar expresiones regulares en la validación del email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

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















































# -- CODIGOS DE PRUEBA --

# -------------------
# -- LOG IN WINDOW --
# -------------------



# def login_multiple_thirdparty() -> rx.Component:
#     return rx.center(  # Asegura que la tarjeta esté centrada
#         rx.card(
#             rx.vstack(
#                 rx.flex(
#                     rx.image(
#                         src=("https://github.com/arnaldoquinones/my_portfolio/blob/master/assets/foto_perfil.png?raw=true"),
#                         width="2.5em",
#                         height="auto",
#                         border_radius="25%",
#                     ),
#                     rx.heading(
#                         "Sign in to your account",
#                         size="6",
#                         as_="h2",
#                         width="100%",
#                     ),
#                     rx.hstack(
#                         rx.text(
#                             "New here?",
#                             size="3",
#                             text_align="left",
#                         ),
#                         rx.link("Sign up", href="#", size="3"),
#                         spacing="2",
#                         opacity="0.8",
#                         width="100%",
#                     ),
#                     justify="start",
#                     direction="column",
#                     spacing="4",
#                     width="100%",
#                 ),
#                 rx.vstack(
#                     rx.text(
#                         "Email address",
#                         size="3",
#                         weight="medium",
#                         text_align="left",
#                         width="100%",
#                     ),
#                     rx.input(
#                         rx.input.slot(rx.icon("user")),
#                         placeholder="user@reflex.dev",
#                         type="email",
#                         size="3",
#                         width="100%",
#                     ),
#                     spacing="2",
#                     justify="start",
#                     width="100%",
#                 ),
#                 rx.vstack(
#                     rx.hstack(
#                         rx.text(
#                             "Password",
#                             size="3",
#                             weight="medium",
#                         ),
#                         rx.link(
#                             "Forgot password?",
#                             href="#",
#                             size="3",
#                         ),
#                         justify="between",
#                         width="100%",
#                     ),
#                     rx.input(
#                         rx.input.slot(rx.icon("lock")),
#                         placeholder="Enter your password",
#                         type="password",
#                         size="3",
#                         width="100%",
#                     ),
#                     spacing="2",
#                     width="100%",
#                 ),
#                 rx.button("Sign in", size="3", width="100%"),
#                 rx.hstack(
#                     rx.divider(margin="0"),
#                     rx.text(
#                         "Or continue with",
#                         white_space="nowrap",
#                         weight="medium",
#                     ),
#                     rx.divider(margin="0"),
#                     align="center",
#                     width="100%",
#                 ),
#                 rx.center(
#                     rx.icon_button(
#                         rx.icon(tag="github"),
#                         variant="soft",
#                         size="3",
#                     ),
#                     rx.icon_button(
#                         rx.icon(tag="facebook"),
#                         variant="soft",
#                         size="3",
#                     ),
#                     rx.icon_button(
#                         rx.icon(tag="twitter"),
#                         variant="soft",
#                         size="3",
#                     ),
#                     spacing="4",
#                     direction="row",
#                     width="100%",
#                 ),
#                 spacing="6",
#                 width="100%",
#             ),
#             size="2",
#             max_width="24em",  # Tamaño ajustado para que no sea tan ancho
#             width="50%",       # Ajusta el porcentaje del ancho
#             background_color="#4a90e2",  # Fondo azul
#             padding="2em",     # Espaciado interno
#             border_radius="1em",  # Bordes redondeados
#             shadow="5",       # Añade sombra para profundidad
#         ),
#         height="100vh",  # Asegura que el contenedor use toda la altura disponible
#         align_items="center",
#         justify_content="center",
#     )






# def suma(a,b):
#     c=a+b
#     return print (c)

# if __name__ == "__main__":
#     suma(7,8)
