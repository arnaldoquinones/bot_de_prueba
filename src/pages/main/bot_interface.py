import reflex as rx
from .modulos import SidebarState

class State(rx.State):
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    window_open: bool = True  # Variable para controlar la visibilidad de la ventana
    
    def submit_message(self):
        """Método auxiliar para procesar el mensaje."""
        if self.question.strip():
            answer = f"Respuesta a: {self.question}"
            self.chat_history.append((self.question, answer))
            self.question = ""
    
    @rx.event
    async def answer(self):
        self.submit_message()
        yield
    
    @rx.event
    async def handle_key_down(self, key: str):
        if key == "Enter":
            self.submit_message()
        yield

    @rx.event
    def close_window(self):
        """Cerrar la ventana (ocultarla)"""
        self.window_open = False  # Cambia el estado de la ventana para cerrarla
    # Cambia el estado de la ventana para cerrarla

shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "5%"

# Estilo minimalista para la barra de desplazamiento
scrollbar_style = {
    "&::-webkit-scrollbar": {
        "width": "6px",  # Ancho más delgado
    },
    "&::-webkit-scrollbar-thumb": {
        "background-color": "rgba(255, 255, 255, 0.1)",  # Color más sutil
        "border-radius": "3px",
    },
    "&::-webkit-scrollbar-track": {
        "background": "transparent",  # Track invisible
    },
    "scrollbar-width": "thin",
    "scrollbar-color": "rgba(255, 255, 0.1) transparent",
    "&:hover": {
        "&::-webkit-scrollbar-thumb": {
            "background-color": "rgba(255, 255, 255, 0.2)",  # Un poco más visible al hover
        }
    }
}

message_style = dict(
    padding="0.8em",
    border_radius="5px",
    margin_y="0.4em",
    box_shadow=shadow,
    max_width="90%",
    display="inline-block",
)

question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4),
)

answer_style = message_style | dict(
    margin_right=chat_margin,
    background_color=rx.color("accent", 8),
)

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(rx.text(question, style=question_style), text_align="right"),
        rx.box(rx.text(answer, style=answer_style), text_align="left"),
        margin_y="0.8em",
        width="100%",
    )

def chat() -> rx.Component:
    return rx.box(
        rx.box(
            rx.foreach(
                State.chat_history,
                lambda messages: qa(messages[0], messages[1]),
            ),
            width="100%",
            height="100%",
            overflow_y="auto",
            style=scrollbar_style,
        ),
        padding="0.8em",
        height="55vh",
        border_radius="12px",
        bg=rx.color("gray", 1),
        margin_bottom="0.5em",
        margin_top="20px",
        width="100%",
    )

def action_bar() -> rx.Component:
    return rx.vstack(
        rx.input(
            value=State.question,
            placeholder="Ingrese su consulta...",
            on_change=State.set_question,
            on_key_down=State.handle_key_down,
            border_radius="40px",
            width="100%",
            margin_top="-10px",  # Espacio entre la barra de acción y el chat
        ),
        rx.icon(
            tag="send-horizontal",
            margin_right="3%",
            margin_top="-38px",  # Posiciona el ícono sobre la caja de entrada
            align_self="flex-end",
            size=19,
            cursor="pointer",
        ),
        width="100%",
        on_click=State.answer,  # Acción al hacer clic en el ícono
    )

def stackbot() -> rx.Component:
    return rx.stack(
        rx.container(
            # Ventana del chat
            rx.vstack(
                chat(),
                action_bar(),
                spacing="3",
                width="100%",
            ),
            width="300px",  # Tamaño fijo para la ventana
            height="70vh",  # Altura fija para la ventana
            padding="0.8em",
            background_color="rgba(0,0,0,0.4)",  # Fondo translúcido
            backdrop_filter="blur(0px)",  # Efecto de desenfoque en el fondo
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
            position="relative",  # Necesario para que el ícono se posicione correctamente
            visibility=rx.cond(SidebarState.chatbot_window_open, "visible", "hidden")
        ),
        # Ícono de cierre (en la parte superior derecha de la ventana)
        rx.cond(
            SidebarState.chatbot_window_open,  # Solo muestra el ícono si la ventana está abierta
            rx.icon(
                tag="x",  # Ícono de cierre
                size=24,
                cursor="pointer",
                on_click=State.close_window,  # Aquí se dispara el evento
                position="absolute",
                top="10px",  # Distancia desde el borde superior
                right="10px",  # Distancia desde el borde derecho
                color="white",  # Asegúrate de que el ícono tenga un color visible
                z_index=10  # Asegura que el ícono esté sobre otros elementos
            ),
            None  # Si la ventana está cerrada, no se muestra el ícono
        ),
        position="absolute",  # Posiciona el contenedor de forma absoluta
        bottom="2%",  # Distancia desde el borde inferior
        right="40%",  # Distancia desde el borde derecho
    )
