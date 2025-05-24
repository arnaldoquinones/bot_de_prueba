import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message
import asyncio
from .bot_interface import stackbot


def about() -> rx.Component:
    """Página About me."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
                rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("About me"),
                        ),
                        size="6")
                    ),
                        rx.image(
                                src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                                width="120px",
                                height="auto",
                                border_radius="50%",
                                alt="Foto de perfil",
                                margin_top="-24px",
                                margin_left="-12em",
                                animation="neonGlow 2s infinite alternate cubic-bezier(0.455, 0.030, 0.515, 0.955)",
                                style={
                                    "@keyframes neonGlow": {
                                        "0%": {
                                            "filter": "drop-shadow(0 0 10px rgba(255,255,255,.3)) drop-shadow(0 0 20px rgba(255,255,255,.3)) drop-shadow(0 0 40px rgba(66,220,219,.3)) drop-shadow(0 0 60px rgba(66,220,219,.3))"
                                        },
                                        "100%": {
                                            "filter": "drop-shadow(0 0 2px rgba(255,255,255,.2)) drop-shadow(0 0 8px rgba(255,255,255,.2)) drop-shadow(0 0 20px rgba(66,220,219,.2)) drop-shadow(0 0 30px rgba(66,220,219,.2))"
                                        }
                                    }
                                }
                            ),
                pop_up_message(),
                padding="1em",
                flex="1",
            ),
            stackbot(),
            sidebar_bottom_profile(),
        ),
        min_height="100vh",
        width="100vw",
        background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/circuito_fondo.png?raw=true')",
        background_size="cover",  # Ajusta el tamaño de la imagen para cubrir todo el fondo
        background_repeat="no-repeat",  # Evita que la imagen se repita
        background_position="center",  # Centra la imagen en el fondo
        overflow_y="auto",
        # background="linear-gradient(to bottom, #002266, #001122)",
        # overflow_y="auto",
    )

