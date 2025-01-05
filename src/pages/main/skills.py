import reflex as rx
from rxconfig import config
from .modulos import sidebar_bottom_profile, pop_up_message
# from .chatbot import chat  # Importa el componente del chatbot


def skills() -> rx.Component:
    """Página Skills."""
    return rx.box(
        rx.hstack(
            sidebar_bottom_profile(),  # Barra lateral
            rx.container(
                rx.vstack(
                    rx.heading("Skills Page", size="3", color="white"),
                    rx.text(
                        "Let me show you my skills.",
                        size="5",
                        color="gray.200",
                        text_align="center",
                    ),
                    rx.container(
                        # chat(),  # Aquí integras el chatbot
                        # padding="1em",
                        # border_radius="10px",
                        # background="white",
                        # box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                        # margin_top="2em",
                        # width="80%",  # Ajusta el ancho según prefieras
                        # align_self="center",  # Centra horizontalmente dentro del vstack
                    ),
                    spacing="5",  # Espaciado entre elementos del vstack
                    justify="center",  # Centra el contenido verticalmente
                ),
                padding="1em",  # Margen interno
                flex="1",  # Permite que el contenedor ocupe el espacio disponible
            ),
            pop_up_message(),  # Mueve el pop-up fuera del contenedor principal
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )
