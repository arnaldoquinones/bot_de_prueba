import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message
# from .chatbot import chat  # Importa el componente del chatbot


def skills() -> rx.Component:
    """Skills page."""
    return rx.box(
        header(),  # Encabezado principal
        # Contenedor principal con diseño de columnas
        rx.hstack(
            # Imagen del perfil
            rx.image(
                                src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                                width="120px",
                                height="auto",
                                border_radius="50%",
                                alt="Foto de perfil",
                                margin_top="-58px",
                                margin_left="-11.9em",
                            ),
            # Contenido principal
            rx.container(
                rx.vstack(
                    rx.heading("Skills", size="6", color="white"),
                    spacing="4",
                ),
                width="70%",
                padding="2rem",
            ),
            # Sidebar y mensajes emergentes
            rx.box(
                sidebar_bottom_profile(),  # Sidebar
                pop_up_message(),  # Mensaje emergente
                width="20%",  # Ajusta el tamaño del contenedor
                padding="1rem",
            ),
            spacing="4",  # Espaciado entre columnas
            justify="between",
            align="start",
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )



# Define the style with animations
# style = {
#     "@keyframes slideIn": {
#         "0%": {"transform": "translateX(-100%)", "opacity": "0"},
#         "100%": {"transform": "translateX(0)", "opacity": "1"}
#     },
#     "@keyframes fadeIn": {
#         "from": {"opacity": "0"},
#         "to": {"opacity": "1"}
#     },
#     ".slide-in": {
#         "animation": "slideIn 1s ease-out forwards"
#     },
#     ".fade-in": {
#         "animation": "fadeIn 2s ease-in-out forwards"
#     }
# }
# import reflex as rx

# # First define our state


# class State(rx.State):
#     """The app state."""
#     text: str = "My Skills"

# def skills() -> rx.Component:
#     return rx.box(
#         rx.vstack(
#             rx.heading(State.text, size="4"),
#             rx.text(
#                 "Python Development",
#                 color="white",
#                 font_size="2em",
#                 # Start with just one simple animation
#                 opacity="0",
#                 _hover={"opacity": "1", "transition": "opacity 2.5s"}
#             ),
#             spacing="4",
#             padding="2em",
#         ),
#         width="100%",
#         min_height="100vh", 
#         background="linear-gradient(to bottom, #002266, #001122)"
#     )

# app = rx.App()
# app.add_page(skills)













# import reflex as rx

# # Define the style with automatic animation
# import reflex as rx

# # Define styles similar to the chat app tutorial
# style = {
#     "animate": {
#         "opacity": "0",
#         "animation": "fadeIn 4s ease-in-out forwards",
#         "@keyframes fadeIn": {
#             "from": {"opacity": "0"},
#             "to": {"opacity": "1"}
#         }
#     }
# }

# class State(rx.State):
#     """The app state."""
#     text: str = "My Skills"

# def skills() -> rx.Component:
#     return rx.box(
#         rx.vstack(
#             rx.heading(State.text, size="4"),
#             rx.text(
#                 "Python Development",
#                 color="white",
#                 font_size="2em",
#                 style=style["animate"]  # Apply style directly
#             ),
#             spacing="4",
#             padding="2em",
#         ),
#         width="100%",
#         min_height="100vh",
#         background="linear-gradient(to bottom, #002266, #001122)"
#     )

# app = rx.App()
# app.add_page(skills)