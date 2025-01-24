import reflex as rx
from rxconfig import config
from .modulos import header,sidebar_bottom_profile, pop_up_message
from .bot_interface import stackbot


def resumen() -> rx.Component:
    """Página Proyects."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Resumen de la busqueda"),
                        ),
                        size="6"
                    ),
                    rx.image(
                                src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                                width="120px",
                                height="auto",
                                border_radius="50%",
                                alt="Foto de perfil",
                                margin_top="-58px",
                                margin_left="-11.9em",
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

