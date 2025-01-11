import reflex as rx


def stackbot() -> rx.Component:
    """Crea un componente personalizado con un contenedor dentro de un stack."""
    return rx.stack(
        rx.flex(
            rx.input(
                rx.input.slot(
                    rx.icon(tag="search"),
                ),
                placeholder="Ingrese consulta",
                border_radius="40px",
            ),
            direction="column",
            spacing="3",
            style={"maxWidth": 500},
            
        ),
        rx.container(
            
            width="270px",
            height="70vh",
            center_content=True,
            bg=rx.color("accent", 3),
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
        ),
        position="absolute",  # Posicionamiento absoluto
        bottom="2%",  # Alineado al borde inferior
        right="10%",  # Alineado al borde izquierdo
    )


def chatbot_styles() -> rx.Component:
    return rx.style(
        """
        @keyframes slideInFromBottom {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        """
    )
