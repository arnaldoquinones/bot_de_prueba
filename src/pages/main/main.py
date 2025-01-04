"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    pass
    

intro_texto_castellano = """Con más de 24 años de experiencia en el ambito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el area administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas."""

intro_texto_ingles = """With more than 24 years of experience in the financial banking sector, I have held roles in both the administrative and commercial areas, specifically as an account and business officer. During my time in the administrative area, I acquired significant skills in the preparation of reports using DDB tools, thus contributing to operational efficiency and informed decision-making."""

def index() -> rx.Component:
    """Componente principal que renderiza la vista principal de la app."""
    return rx.box(
        rx.hstack(
            # sidebar_bottom_profile(),
            # rx.color_mode.button(position="top-right"),
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Data scientist"),
                            rx.text("& Data analyst"),
                        ),
                        size="6"
                    ),
                    rx.box(  # Contenedor de texto
                        rx.text(
                            """ "...Scientia est potentia..." """,
                            font_size="1.2em",
                            font_style="italic",
                            text_align="right",  # Alinea el texto a la derecha
                            color="white",
                            margin_top="1em",  # Espacio desde la parte superior
                            margin_right="3em",  # Espacio desde la parte derecha
                        ),
                        position="absolute",  # Posicionamiento absoluto
                        top="0",  # Alineado al principio de la parte superior
                        right="0",  # Alineado al principio de la parte derecha
                    ),
                    rx.flex(
                        rx.text(
                            """ Con más de 24 años de experiencia en el ámbito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el área administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas.""",
                            font_size="0.8em"
                        ),
                        position="absolute",  # Posicionamiento absoluto
                        top="4em",
                        justify="center",
                        align_items="center",  # Cambiado 'align' por 'align_items'
                        height="200px",
                        width="400px",
                        text_align="justify",
                        color="white"
                    ),
                    # pop_up_message(),
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
                        rx.button(rx.icon(tag="mail", size=18),
                            "Messages",
                            border_radius="20px",
                            width="120px",
                            # on_click=lambda: State.set_show_popup(True),  # Abre el modal
                        ),
                        spacing="4",
                        align_items="center",  # Cambiado 'align' por 'align_items'
                        position="absolute",  # Hacer que el contenedor esté posicionado de manera absoluta
                        top="16em",  # Ajusta esto según lo que necesites para que los botones suban
                    ),
                    spacing="5",
                    justify_content="center",  # Cambiado 'justify' por 'justify_content'
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

