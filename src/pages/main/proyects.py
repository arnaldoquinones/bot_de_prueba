import reflex as rx
from rxconfig import config
from .modulos import header,sidebar_bottom_profile, pop_up_message


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
                        size="6"
                    ),
                    rx.image(
                        src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                        width="120px",
                        height="auto",
                        border_radius="50%",
                        alt="Foto de perfil",
                        margin_top="-68px",
                        margin_left="-12em",
                    ),
                    spacing="4",  # Usa un valor numérico entre 0 y 9
                ),
                width="80%",  # Ajusta el ancho del contenedor
                padding="2rem",  # Ajusta el padding interno
            ),
            sidebar_bottom_profile(),
            pop_up_message(),  # login_multiple_thirdparty() puede reemplazar esto si es necesario
            spacing="4",  # Ajusta el espaciado entre el contenido
            align="start",  # Alinea el contenido al inicio
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )

