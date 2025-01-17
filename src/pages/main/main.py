import reflex as rx
from rxconfig import config
import asyncio
from .modulos import header, sidebar_bottom_profile, pop_up_message, MessageFormStateV2, sound_effect_script
from .about_me import about
from .resumen import resumen
from .skills import skills
from .proyects import proyects
from .bot_interface import stackbot


# class State(rx.State):
#     pass

class TypewriterState(rx.State):
    text: str = ""
    full_text: str = (
        "Con más de 24 años de experiencia en el ámbito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el área administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas.")

    async def type_text(self):
        for i in range(1, len(self.full_text) + 1):
            self.text = self.full_text[:i]
            await asyncio.sleep(0.0155)  # Velocidad de la animación
            yield


# intro_texto_castellano = """Con más de 24 años de experiencia en el ámbito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el área administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas."""

# intro_texto_ingles = """With more than 24 years of experience in the financial banking sector, I have held roles in both the administrative and commercial areas, specifically as an account and business officer. During my time in the administrative area, I acquired significant skills in the preparation of reports using DDB tools, thus contributing to operational efficiency and informed decision-making."""

@rx.page(on_load=TypewriterState.type_text)  # Aquí se ejecuta la animación cuando se carga la página
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
                        rx.text(TypewriterState.text,
                                font_size="0.8em",),
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
                    #     src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/imagen_perfil_profesional.png?raw=true",  # Cambia esta URL por la de tu imagen
                    #     alt="Descripción de la imagen",
                    #     width="340px",
                    #     height="360px",
                    #     margin_top="-9em",
                    #     margin_left="36em",
                    # ),
                ),
                rx.hstack(
                    rx.link(
                        rx.button(rx.icon(tag="github", size=18), "GitHub", border_radius="20px", width="120px", background_color="#003D73", color="white",_hover={
                        "background_color": rx.color_mode_cond(
                            light="blue.400",
                            dark="blue.500"
                        ),
                        "box_shadow": rx.color_mode_cond(
                            light="0 0 10px blue",
                            dark="0 0 10px rgba(66, 153, 225, 0.6)"
                        ),
                        "transform": "scale(1.05)"
                        },
                        transition="all 0.2s ease-in-out",
                        on_click=rx.call_script("playFromStart(button_sfx)")
                        ),
                        href="https://github.com/arnaldoquinones",
                        is_external=True,
                    ),
                    rx.link(
                        rx.button(rx.icon(tag="linkedin", size=18), "Linkedin", border_radius="20px", width="120px", background_color="#003D73", color="white",_hover={
                        "background_color": rx.color_mode_cond(
                            light="blue.400",
                            dark="blue.500"
                        ),
                        "box_shadow": rx.color_mode_cond(
                            light="0 0 10px blue",
                            dark="0 0 10px rgba(66, 153, 225, 0.6)"
                        ),
                        "transform": "scale(1.05)"
                    },
                    transition="all 0.2s ease-in-out",
                    on_click=rx.call_script("playFromStart(button_sfx)")
                        ),
                                    href="https://www.linkedin.com/in/apquinones/",
                                    is_external=True,
                    ),
                    rx.button(
                    rx.icon(tag="mail", size=18),
                    "Messages",
                    border_radius="20px",
                    width="120px",
                    background_color="#003D73",
                    color="white",
                    _hover={
                        "background_color": rx.color_mode_cond(
                            light="blue.400",
                            dark="blue.500"
                        ),
                        "box_shadow": rx.color_mode_cond(
                            light="0 0 10px blue",
                            dark="0 0 10px rgba(66, 153, 225, 0.6)"
                        ),
                        "transform": "scale(1.05)"
                    },
                    transition="all 0.2s ease-in-out",
                    on_click=[
                        MessageFormStateV2.toggle_popover,  # Mantiene el evento actual
                        rx.call_script("playFromStart(button_sfx)")  # Agrega el sonido
                    ]
                ),
                    spacing="4",
                    align_items="center",
                    position="absolute",
                    top="31em",
                ),
                spacing="5",
                justify_content="center",
                padding="1em",
                flex="1",
           
            ),
            stackbot(),
            sidebar_bottom_profile(),
            pop_up_message(),
        ),
        min_height="100vh",
        width="100vw",
        background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/circuito_fondo.png?raw=true')",
        background_size="cover",  # Ajusta el tamaño de la imagen para cubrir todo el fondo
        background_repeat="no-repeat",  # Evita que la imagen se repita
        background_position="center",  # Centra la imagen en el fondo
        overflow_y="auto",
    )

app = rx.App()
app.add_page(index)
# ---------------------------
# -- ENLACES A LAS PAGINAS --
# ---------------------------
def main_page() -> rx.Component:
    return rx.box(
        rx.link("About Me", href="./about_me"),
        rx.link("Skills", href="./skills"),
        rx.link("Projects", href="./proyects"),
        rx.link("Projects", href="./resumen"),
        # rx.text("Welcome to my Portfolio", size="3", font_weight="bold"),
        # spacing="4",
        # align="center",
        # justify="center",
        # height="100vh",
        # bg="teal.100",
    )

# Add routes for the main page and subpages.
app.add_page(main_page)
app.add_page(about)
app.add_page(skills)
app.add_page(proyects)
app.add_page(index)  # Agregar la página principal.
app.add_page(resumen)  # Agregar la página principal.