import reflex as rx
from rxconfig import config
from .modulos import header,sidebar_bottom_profile, pop_up_message
from .bot_interface import stackbot



def proyects() -> rx.Component:
    """Página Proyects."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("My proyects"),
                        ),
                        size="6",
                        margin_top="-1rem",
                    ),
                    rx.image(
                        src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                        width="120px",
                        height="auto",
                        border_radius="50%",
                        alt="Foto de perfil",
                        margin_top="-40px",
                        margin_left="-11.9em",
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
                    spacing="4",  # Usa un valor numérico entre 0 y 9
                ),
                width="80%",  # Ajusta el ancho del contenedor
                padding="2rem",  # Ajusta el padding interno
            ),
            stackbot(),
            sidebar_bottom_profile(),
            pop_up_message(),  # login_multiple_thirdparty() puede reemplazar esto si es necesario
            spacing="4",  # Ajusta el espaciado entre el contenido
            align="start",  # Alinea el contenido al inicio
        ),
        min_height="100vh",
        width="100vw",
        background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/circuito_fondo.png?raw=true')",
        background_size="cover",  # Ajusta el tamaño de la imagen para cubrir todo el fondo
        background_repeat="no-repeat",  # Evita que la imagen se repita
        background_position="center",  # Centra la imagen en el fondo
        overflow_y="auto",
    )



