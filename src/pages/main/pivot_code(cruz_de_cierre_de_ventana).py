import reflex as rx
from .modulos import SidebarState  # Este módulo debe existir y contener el estado compartido

class State(rx.State):
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    window_open: bool = True  # Controla si la ventana está abierta

    def submit_message(self):
        """Procesar el mensaje del usuario."""
        if self.question.strip():
            answer = f"Respuesta a: {self.question}"
            self.chat_history.append((self.question, answer))
            self.question = ""

    @rx.event
    async def answer(self):
        """Evento que procesa la pregunta y genera una respuesta."""
        self.submit_message()
        yield

    @rx.event
    async def handle_key_down(self, key: str):
        """Detecta la tecla Enter para enviar un mensaje."""
        if key == "Enter":
            self.submit_message()
        yield

    @rx.event
    def toggle_window(self):
        """Alternar la visibilidad de la ventana del chatbot."""
        self.window_open = not self.window_open


# Estilo minimalista para la barra de desplazamiento
scrollbar_style = {
    "&::-webkit-scrollbar": {"width": "6px"},
    "&::-webkit-scrollbar-thumb": {
        "background-color": "rgba(255, 255, 255, 0.1)",
        "border-radius": "3px",
    },
    "&::-webkit-scrollbar-track": {"background": "transparent"},
    "scrollbar-width": "thin",
    "scrollbar-color": "rgba(255, 255, 0.1) transparent",
    "&:hover": {
        "&::-webkit-scrollbar-thumb": {
            "background-color": "rgba(255, 255, 255, 0.2)",
        }
    },
}

# Estilo de los mensajes
message_style = dict(
    padding="0.8em",
    border_radius="5px",
    margin_y="0.4em",
    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
    max_width="90%",
    display="inline-block",
)

question_style = message_style | dict(
    margin_left="5%",
    background_color=rx.color("gray", 4),
)

answer_style = message_style | dict(
    margin_right="5%",
    background_color="linear-gradient(to right, #8e44ad, #e91e63, #3498db)",,
)

def qa(question: str, answer: str) -> rx.Component:
    """Renderiza un par de pregunta-respuesta."""
    return rx.box(
        rx.box(rx.text(question, style=question_style), text_align="right"),
        rx.box(rx.text(answer, style=answer_style), text_align="left"),
        margin_y="0.8em",
        width="100%",
    )

def chat() -> rx.Component:
    """Área de chat."""
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

def render_chat_window() -> rx.Component:
    """Renderiza la ventana del chatbot."""
    if SidebarState.chatbot_window_open:
        return rx.box(
            rx.text("Este es el chatbot"),
            bg="gray.100",
            padding="1em",
            border_radius="lg",
        )
    return rx.box()  # Si el chatbot no está abierto, no muestra nada

def action_bar() -> rx.Component:
    """Barra de acción del chat."""
    return rx.vstack(
        rx.input(
            value=State.question,
            placeholder="Ingrese su consulta...",
            on_change=State.set_question,
            on_key_down=State.handle_key_down,
            border_radius="40px",
            width="100%",
            margin_top="-10px",
        ),
        rx.icon(
            tag="send-horizontal",
            margin_right="3%",
            margin_top="-38px",
            align_self="flex-end",
            size=19,
            cursor="pointer",
            on_click=State.answer,
        ),
        width="100%",
    )

def stackbot() -> rx.Component:
    """Ventana del chatbot."""
    return rx.stack(
        rx.container(
            rx.vstack(
                chat(),
                action_bar(),
                spacing="3",
                width="100%",
            ),
            width="300px",
            height="70vh",
            padding="0.8em",
            background_color="rgba(0,0,0,0.4)",
            backdrop_filter="blur(0px)",
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
            position="relative",
            visibility=rx.cond(State.window_open, "visible", "hidden"),
        ),
        rx.cond(
            State.window_open,
            rx.icon(
                tag="x",
                size=24,
                cursor="pointer",
                on_click=State.toggle_window,
                position="absolute",
                top="10px",
                right="10px",
                color="white",
                z_index=10,
            ),
            None,
        ),
        position="absolute",
        bottom="2%",
        right="40%",
    )

def sidebar() -> rx.Component:
    """Sidebar con el botón para abrir el chatbot."""
    return rx.box(
        rx.button(
            "Abrir Chatbot",
            on_click=State.toggle_window,
        ),
        position="fixed",
        left="0",
        top="50%",
        transform="translateY(-50%)",
    )

def main_layout() -> rx.Component:
    """Diseño principal de la aplicación."""
    return rx.vstack(
        sidebar(),
        render_chat_window(),
    )
