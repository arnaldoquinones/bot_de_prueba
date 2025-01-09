import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message


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
                                margin_top="-26px",
                                margin_left="-12em",
                            ),
                pop_up_message(),
                padding="1em",
                flex="1",
            ),
            sidebar_bottom_profile(),
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )



# END
