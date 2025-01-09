import asyncio
import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message
# from .chatbot import chat  # Importa el componente del chatbot


# Definir la función de "Skills" (Páginas)
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
        background="linear-gradient(to bottom, #002266, #001122)",
        overflow_y="auto",
    )


# Definir el estado para la animación de texto
class State(rx.State):
    text: str = ""  # Inicializar el estado con texto vacío
    
    # Función para simular el efecto de máquina de escribir
    async def type_text(self):
        full_text = """Con más de 24 años de experiencia en el ámbito bancario financiero, he desempeñado roles tanto en el área administrativa como en el comercial, específicamente como oficial de cuentas y negocios. Durante mi tiempo en el área administrativa adquirí habilidades significativas en la preparación de informes empleando herramientas de BDD, contribuyendo así a la eficiencia operativa y la toma de decisiones informadas."""
        
        self.text = ""  # Inicia el texto vacío
        yield
        
        # Agregar el texto caracter por caracter
        for i in range(len(full_text)):
            await asyncio.sleep(0.1)  # Controla la velocidad de la escritura
            self.text = full_text[:i + 1]
            yield


# Función para mostrar el efecto de máquina de escribir en la página de inicio
def index():
    # Crear una instancia del estado para ejecutar type_text automáticamente
    state = State()
    
    return rx.box(
        rx.text(state.text),  # Mostrar el texto que se va actualizando
        state.type_text()  # Iniciar el efecto de escritura automáticamente
    )
