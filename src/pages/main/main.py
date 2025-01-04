import reflex as rx

from rxconfig import config


class State(rx.State):
    pass


def header():
    """Encabezado personalizado para el sitio web."""
    return rx.box(
        rx.heading(
            "My Personal Portfolio",  # Texto del encabezado
            size="3",  # Tamaño del texto
            color="white",  # Cambia el color del texto
        ),
        background_color="blue",  # Fondo del encabezado
        width="100%",  # Ocupa todo el ancho de la pantalla
        height="100px",  # Altura del encabezado
        display="flex",  # Usamos flex para centrar el texto
        justify_content="center",  # Centrado horizontal
        align_items="center",  # Centrado vertical
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
                    rx.box(
                        rx.text(
                            """ "...Scientia est potentia..." """,
                            font_size="1.2em",
                            font_style="italic",
                            text_align="right",
                            color="white",
                            margin_top="1em",
                            margin_right="3em",
                        ),
                        position="absolute",
                        top="0",
                        right="0",
                    ),
                    rx.flex(
                        rx.text(
                            intro_texto_castellano,
                            font_size="0.8em"
                        ),
                        position="absolute",
                        top="4em",
                        justify="center",
                        align_items="center",
                        height="200px",
                        width="400px",
                        text_align="justify",
                        color="white"
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
                        top="16em",
                    ),
                    spacing="5",
                    justify_content="center",
                ),
                padding="1em",
                flex="1",
            ),
        ),
        min_height="100vh",
        width="100vw",
        background="linear-gradient(to bottom, #000066, #000000)",
        overflow_y="auto",
    )


app = rx.App()
app.add_page(index)

