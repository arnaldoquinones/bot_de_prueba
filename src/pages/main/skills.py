import asyncio
import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message


class TypewriterState(rx.State):
    text: str = ""
    full_text: str = (
        "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum"
    )

    async def type_text(self):
        for i in range(1, len(self.full_text) + 1):
            self.text = self.full_text[:i]
            await asyncio.sleep(0.01565)  # Velocidad de la animación
            yield


# Definir la función de "Skills" (Páginas)
@rx.page(on_load=TypewriterState.type_text)  # Aquí se ejecuta la animación cuando se carga la página
def skills() -> rx.Component:
    """Página Projects."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Skills"),
                        ),
                        size="6"
                    ),
                    rx.image(
                        src="https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/logo_fondo_transparente.png?raw=true",
                        width="120px",
                        height="auto",
                        border_radius="50%",
                        alt="Foto de perfil",
                        margin_top="-58px",
                        margin_left="-11.9em",
                    ),
                    # Aquí se aplica el efecto de la animación tipo escritura sin el cursor
                    rx.box(
                        rx.text(TypewriterState.text),  # Texto animado
                        position="absolute",  # Evita que el texto afecte la posición de los demás
                        top="350px",  # Ajusta la posición del texto
                        left="240px",  # Ajusta la distancia desde la izquierda
                        width="80%",  # Ajusta el ancho del contenedor de texto
                        padding="1rem",
                        text_align="justify",
                        z_index=10,  # Asegura que el texto esté por encima de otros elementos si es necesario
                    ),
                    spacing="4",  # Usa un valor numérico entre 0 y 9
                ),
                width="80%",  # Ajusta el ancho del contenedor
                padding="2rem",  # Ajusta el padding interno
            ),
            sidebar_bottom_profile(),
            pop_up_message(),  # login_multiple_thirdparty() puede reemplazar esto si es necesario
            spacing="4",  # Ajusta el espaciado entre el contenido
            align="start",  # Alinea el contenido al inicio
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
