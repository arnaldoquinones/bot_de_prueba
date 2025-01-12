import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message
import asyncio


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
            stackbot2(),
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


def stackbot2() -> rx.Component:
    """Crea un componente personalizado con un contenedor dentro de un stack."""
    return rx.stack(
           rx.flex(
            rx.input(
                placeholder="Ingrese consulta",
                margin_right="-590px",
                border_radius="40px",
                width="290px",
            ),
        rx.icon(
                tag="send-horizontal",
                margin_right="-40px",
                align_self="center",
                size=19  # Use integers for size instead of font_size
        ),
            direction="row",
            spacing="4",  # Valor permitido para spacing
            align="center",
            style={"maxWidth": "320px"},  # Ajuste para contener ambos elementos
            position="relative",  # Asegura que los elementos se posicionen correctamente
            top="10px",  # Ajuste para separarlo del borde superior
        ),
        rx.container(
            width="300px",
            height="70vh",
            center_content=True,
            background="rgba(255, 255, 255, 0.3)",  # Fondo translúcido con menos opacidad
            backdrop_filter="blur(4px)",  # Difuminado reducido
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3)",  # Sombra ligera
            padding="20px",  # Espaciado interno para mejor visualización
        ),
        position="absolute",  # Posicionamiento absoluto
        bottom="2%",  # Alineado al borde inferior
        right="10%",  # Alineado al borde derecho
    )




