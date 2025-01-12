import reflex as rx


def stackbot() -> rx.Component:
    """Crea un componente personalizado con un contenedor dentro de un stack."""
    return rx.stack(
        rx.flex(
    rx.input(
        placeholder="Ingrese consulta",
        border_radius="40px",
        width="245px",
    ),
    rx.icon(
        tag="send-horizontal",
        margin_left="-40px", # Push icon to overlap with input
        align_self="center", # Center vertically
    ),
    direction="row",
    spacing="0", # Remove spacing between input and icon
    align="center", # Center items vertically
    style={"maxWidth": 700},
    position="relative",
    top="375px",
    left="255px",
),
        rx.container(
    width="270px",
    height="70vh",
    center_content=True,
    background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/fondo_chatbot.jpg?raw=true') center/cover",  # Corregido el uso de la URL y la propiedad
    border_radius="15px",
    box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
),

        position="absolute",  # Posicionamiento absoluto para el contenedor principal
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
