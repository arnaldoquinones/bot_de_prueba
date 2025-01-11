import reflex as rx


def stackbot() -> rx.Component:
    """Crea un componente personalizado con un contenedor dentro de un stack."""
    return rx.stack(
        rx.text("Chatbot", size="2xl", color="white"),
        rx.container(
            width="200px",
            height="75vh",
            center_content=True,
            bg=rx.color("accent", 3),
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
        ),
        position="absolute",  # Posicionamiento absoluto
        bottom="2%",  # Alineado al borde inferior
        right="10%",  # Alineado al borde izquierdo
    )
