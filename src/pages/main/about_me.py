import reflex as rx
from rxconfig import config
# from .modulos import sidebar_bottom_profile, pop_up_message


def about() -> rx.Component:
    """Página About me."""
    return rx.box(
        rx.hstack(
            sidebar_bottom_profile(),  # Barra lateral
            rx.container(
                rx.vstack(
                    rx.heading("About me.", size="3", color="white"),
                    rx.text(
                        "Hello! I am Arnaldo, a professional in data analysis, system design, and development.",
                        size="5",
                        color="gray.200",
                        text_align="center",
                    ),
                    spacing="5",
                    justify="center",
                ),
                rx.image(
                        src="https://github.com/arnaldoquinones/portfolio/blob/master/assets/foto_perfil.png?raw=true",
                        width="150px",
                        height="auto",
                        border_radius="50%",
                        alt="Foto de perfil",
                    ),
                pop_up_message(),
                padding="1em",
                flex="1",
            ),
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )



# END
