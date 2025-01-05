import reflex as rx
from rxconfig import config

class State(rx.State):
    pass

def header():
    """Encabezado personalizado para el sitio web."""
    return rx.box(
        # Caja contenedora general
        rx.flex(
            # Contenedor del icono alineado a la izquierda
            rx.box(
                rx.icon("menu", size=40, margin_top="0.8em", margin_left="2em"),  # Icono a la izquierda
                align="start",  # Alinea el icono al inicio del contenedor
                flex="none"  # No permite que el contenedor ocupe espacio extra
            ),
            # Contenedor centrado para el logo y el título
            rx.flex(
                # Título centrado
                rx.heading(
                    "My Portfolio",  # Título del encabezado
                    size="9",
                    color="white",
                ),
                gap="2",  # Espaciado entre la imagen y el texto
                align="center",  # Alinea el contenido verticalmente
                justify="center",  # Centra horizontalmente
                flex="1",  # Esto permite que este contenedor ocupe el espacio disponible y centre su contenido
                direction="column",  # Coloca los elementos uno debajo del otro
            ),
            gap="2",  # Espaciado entre el icono y el encabezado
            align_items="center",  # Centrado vertical de los elementos
            width="100%",  # Ancho total
            justify_content="flex-start",  # Mantiene los elementos al principio en el eje horizontal
            flex_direction="row",  # Distribuye los elementos en una fila
        ),
        # Caja con la cita
        rx.box(
            rx.text(
                """ "...Scientia est potentia..." """,
                font_size="1.5em",
                font_style="italic",
                text_align="right",
                color="white",
                margin_top="3em",
                margin_right="2em",
            ),
            position="absolute",
            top="0",
            right="0",
        ),
        background_image="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/banner_header.jpg?raw=true')",
        background_size="cover",
        width="100%",
        height="190px",
        display="flex",
        justify_content="center",  # Centra horizontalmente
        align_items="center",  # Centra verticalmente
        box_shadow="0px 10px 20px rgba(0, 0, 0, 0.7), 0px 0px 10px transparent",  # Sombra más grande y oscura
    )

intro_texto_castellano = """Con más de 24 años de experiencia en el ámbito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el área administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas."""

intro_texto_ingles = """With more than 24 years of experience in the financial banking sector, I have held roles in both the administrative and commercial areas, specifically as an account and business officer. During my time in the administrative area, I acquired significant skills in the preparation of reports using DDB tools, thus contributing to operational efficiency and informed decision-making."""

def index() -> rx.Component:
    """Componente principal que renderiza la vista principal de la app."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Data scientist"),
                            rx.text("& Data analyst"),
                        ),
                        size="6"
                    ),
                    rx.flex(
                        rx.text(
                            intro_texto_castellano,
                            font_size="0.8em",
                        ),
                        position="absolute",
                        top="10em",
                        justify="center",
                        align_items="center",
                        height="420px",
                        width="400px",
                        text_align="justify",
                        color="white"
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
                        # rx.image(
                        #     src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/imagen_main.png?raw=true",  # Cambia esta URL por la de tu imagen
                        #     alt="Descripción de la imagen",
                        #     width="340px",
                        #     height="360px",
                        #     margin_top="-6em",
                        #     margin_left="36em",
                        # ),
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(rx.icon(tag="github", size=18), "GitHub", border_radius="20px", width="120px"),
                            href="https://github.com/arnaldoquinones",
                            is_external=True,
                        ),
                        rx.link(
                            rx.button(rx.icon(tag="linkedin", size=18), "Linkedin", border_radius="20px", width="120px"),
                            href="https://www.linkedin.com/in/apquinones/",
                            is_external=True,
                        ),
                        rx.button(
                            rx.icon(tag="mail", size=18),
                            "Messages",
                            border_radius="20px",
                            width="120px",
                        ),
                        spacing="4",
                        align_items="center",
                        position="absolute",
                        top="30em",
                    ),
                    spacing="5",
                    justify_content="center",
                ),
                padding="1em",
                flex="1",
            ),
        
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #000066, #000000)",
        overflow_y="auto",
    )

app = rx.App()
app.add_page(index)
