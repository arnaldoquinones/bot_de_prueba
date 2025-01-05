import reflex as rx
from rxconfig import config
from .modulos import sidebar_bottom_profile, pop_up_message


def proyects() -> rx.Component:
    """Página Proyects."""
    return rx.box(
        rx.hstack(
            sidebar_bottom_profile(),  # Barra lateral
            rx.container(
                rx.vstack(
                    rx.heading("Proyects Page", size="3", color="white"),
                    rx.text(
                        "Those are my works.",
                        size="5",
                        color="gray.200",
                        text_align="center",
                    ),
                    spacing="5",
                    justify="center",
                ),
                padding="1em",
                flex="1",
            ),
            pop_up_message(),# login_multiple_thirdparty(),
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )