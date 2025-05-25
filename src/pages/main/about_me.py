import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message
import asyncio
from .bot_interface import stackbot

style = {
    "animate": {
        "opacity": "0",
        "animation": "fadeIn 4s ease-in-out forwards",
        "@keyframes fadeIn": {
            "from": {"opacity": "0"},
            "to": {"opacity": "1"}
        }
    }
}
class TypewriterState2(rx.State):
    text: str = ""
    full_text: str = (
        "Actualmente me encuentro desempeñando funciones como analista de datos en el Municipio de Pilar, donde estoy diseñando pipelines de procesamiento de datos para automatizar y optimizar la recolección, transformación y carga de información clave. También desarrollo paneles de control interactivos y completos para reportes estratégicos, facilitando la visualización de indicadores y la toma de decisiones en distintas áreas de gobierno. A su vez, realizo análisis orientados al seguimiento de KPIs y la identificación de tendencias de rendimiento, lo que permite anticipar necesidades, mejorar la eficiencia operativa y fortalecer la planificación a mediano y largo plazo."
    "Previamente, me desempeñé como analista de datos en el sector financiero, en el Banco, donde adquirí experiencia en el manejo de grandes volúmenes de datos sensibles, implementando soluciones analíticas para evaluación de riesgo, segmentación de clientes y detección de patrones de comportamiento financiero. Este entorno altamente regulado me permitió desarrollar una sólida capacidad de análisis, precisión en el manejo de la información y enfoque en la seguridad de los datos.")

    async def type_text(self):
        for i in range(1, len(self.full_text) + 1):
            self.text = self.full_text[:i]
            await asyncio.sleep(0.0155)  # Velocidad de la animación
            yield

def about() -> rx.Component:
    """Página About me."""
    return rx.box(
        header(),
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("About me"),
                        ),
                        size="6")
                    ),
                    rx.flex(
                        rx.text(TypewriterState2.text,
                                font_size="0.8em",
                                on_mount=TypewriterState2.type_text),  # Añadir esta línea

                        position="absolute",
                        top="11em",
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
                                margin_top="-24px",
                                margin_left="-12em",
                                animation="neonGlow 2s infinite alternate cubic-bezier(0.455, 0.030, 0.515, 0.955)",
                                style={
                                    "@keyframes neonGlow": {
                                        "0%": {
                                            "filter": "drop-shadow(0 0 10px rgba(255,255,255,.3)) drop-shadow(0 0 20px rgba(255,255,255,.3)) drop-shadow(0 0 40px rgba(66,220,219,.3)) drop-shadow(0 0 60px rgba(66,220,219,.3))"
                                        },
                                        "100%": {
                                            "filter": "drop-shadow(0 0 2px rgba(255,255,255,.2)) drop-shadow(0 0 8px rgba(255,255,255,.2)) drop-shadow(0 0 20px rgba(66,220,219,.2)) drop-shadow(0 0 30px rgba(66,220,219,.2))"
                                        }
                                    }
                                }
                            ),
                pop_up_message(),
                padding="1em",
                flex="1",
            ),
            rx.stack(
                       rx.container(
                           rx.heading(
        "My timeline career",
        size="4",  # Ajusta el tamaño de 1 a 9
        color="white", # Puedes cambiar el color
        margin_bottom="1em", # Espacio debajo del título
        text_align="center", # Para centrar el texto dentro del heading
        style=style["animate"]
    ),
                           width="600px",
                           height="59vh",
                            center_content=True,
                            bg=rx.color("accent", 3),
                            border_radius="15px",
                           box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
                          ),
                         position="absolute",  # Posicionamiento absoluto
                         bottom="6%",  # Alineado al borde inferior
                         right="5%",  # Alineado al borde izquierdo
                     ),
            stackbot(),
            sidebar_bottom_profile(),
            style=style["animate"]
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



# --- Componente de Scroll Horizontal ---   


rx.scroll_area(
    rx.hstack(
        # Aquí tus elementos
    ),
    scrollbars="horizontal",
    style={"width": 400, "height": 150},
)

rx.button("←", on_click=rx.call_script("document.getElementById('mi-scroll').scrollLeft -= 100"))
rx.button("→", on_click=rx.call_script("document.getElementById('mi-scroll').scrollLeft += 100"))


# --- Animación CSS para el efecto de brillo ---
# Puedes definir esto una vez y reutilizarlo
NEON_GLOW_ANIMATION = {
    "@keyframes neonGlow": {
        "0%": {
            "filter": "drop-shadow(0 0 5px rgba(66,220,219,0.5)) drop-shadow(0 0 10px rgba(66,220,219,0.3))"
        },
        "100%": {
            "filter": "drop-shadow(0 0 15px rgba(66,220,219,0.8)) drop-shadow(0 0 30px rgba(66,220,219,0.5))"
        }
    }
}

# --- Componente para un Punto de Evento Brillante ---
def timeline_event_point() -> rx.Component:
    return rx.circle(
        size="3", # Tamaño del círculo del punto
        bg="cyan", # Color de fondo del círculo
        border="2px solid white", # Borde del círculo
        animation="neonGlow 1.5s ease-in-out infinite alternate", # Aplicar la animación de brillo
        style=NEON_GLOW_ANIMATION # Definir los keyframes para la animación
    )

# --- Componente para un Item de la Línea Temporal (el contenido del evento) ---
def timeline_item(text: str, is_left: bool = True) -> rx.Component:
    """
    Crea un item de la línea temporal con un cuadro de texto.
    is_left: True si el texto está a la izquierda del punto, False si está a la derecha.
    """
    return rx.hstack(
        # Espacio para alinear el texto si está a la derecha
        rx.spacer() if not is_left else rx.fragment(),
        rx.box(
            rx.text(text, color="white", font_size="1.1em"),
            bg="rgba(0, 50, 50, 0.6)", # Fondo semitransparente oscuro
            padding="1em",
            border_radius="10px",
            border="1px solid rgba(66,220,219,0.5)", # Borde sutil brillante
            max_width="400px", # Limita el ancho del texto
            box_shadow="0 0 10px rgba(66,220,219,0.3)", # Sombra para un brillo sutil
            _hover={
                "box_shadow": "0 0 20px rgba(66,220,219,0.7)", # Brillo más intenso al pasar el ratón
                "transform": "scale(1.02)", # Pequeña escala para el efecto hover
                "transition": "all 0.2s ease-in-out", # Transición suave
            },
        ),
        # Espacio para alinear el texto si está a la izquierda
        rx.spacer() if is_left else rx.fragment(),
        width="100%", # Asegura que el hstack ocupe todo el ancho disponible
        justify= "end" if is_left else "start" # Alinea el contenido a la izquierda o derecha
    )

# --- Página Principal con la Línea Temporal ---
def timeline_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("My Timeline Carrier", size="7", color="cyan", margin_bottom="2em", text_align="center"),
            rx.hstack(
                # Lado izquierdo de la línea temporal (para items a la izquierda)
                rx.vstack(
                    timeline_item("Inicio de mi carrera en el sector bancario. Aprendizaje de fundamentos.", is_left=True),
                    rx.spacer(), # Espacio para alinear con el punto
                    timeline_item("Especialización en análisis de riesgos crediticios y gestión de cartera.", is_left=True),
                    rx.spacer(),
                    timeline_item("Desarrollo de habilidades en Power BI y Tableau para informes de negocio.", is_left=True),
                    rx.spacer(),
                    width="45%", # Ancho del lado izquierdo
                    align_items="end", # Alinea los ítems a la derecha para que estén cerca de la línea
                    spacing="6em", # Espacio entre los ítems de la línea
                ),

                # La Línea Temporal Vertical Brillante
                rx.box(
                    width="4px", # Grosor de la línea
                    height="100%", # Altura de la línea (se expandirá con el contenido del vstack)
                    bg="cyan", # Color de la línea
                    border_radius="2px",
                    animation="neonGlow 1.5s ease-in-out infinite alternate", # Animación de brillo para la línea
                    style=NEON_GLOW_ANIMATION, # Definir los keyframes
                    position="relative", # Para posicionar los puntos absolutos si fuera necesario
                    margin_x="2em", # Margen a los lados de la línea
                ),

                # Lado derecho de la línea temporal (para items a la derecha)
                rx.vstack(
                    rx.spacer(), # Espacio para alinear con el punto
                    timeline_item("Rol como oficial de cuentas y negocios, enfocado en relaciones con clientes.", is_left=False),
                    rx.spacer(),
                    timeline_item("Implementación de Python para la automatización de análisis de datos.", is_left=False),
                    rx.spacer(),
                    timeline_item("Liderazgo de proyectos para optimizar la eficiencia operativa.", is_left=False),
                    width="45%", # Ancho del lado derecho
                    align_items="start", # Alinea los ítems a la izquierda para que estén cerca de la línea
                    spacing="6em", # Espacio entre los ítems de la línea
                ),
                justify="center", # Centra el hstack completo
                align_items="stretch", # Hace que los vstacks se estiren para la línea
                width="80%", # Ancho del contenedor principal de la línea temporal
                min_height="600px", # Altura mínima para la línea temporal
            ),
            width="100%",
            padding="2em",
            # Estilos de fondo para la página, puedes reutilizar los que ya tienes
            background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/circuito_fondo.png?raw=true')",
            background_size="cover",
            background_repeat="no-repeat",
            background_position="center",
        ),
        min_height="100vh",
        width="100vw",
        overflow_y="auto",
    )

# --- Configuración de la Aplicación Reflex ---
app = rx.App()
app.add_page(timeline_page, route="/timeline") # Añade la página al router, accesible en /timeline