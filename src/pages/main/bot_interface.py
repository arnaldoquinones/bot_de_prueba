import reflex as rx

# Estado global de la aplicación
class State(rx.State):
    # Pregunta actual que se está ingresando
    question: str = ""
    # Historial del chat como una lista de tuplas (pregunta, respuesta)
    chat_history: list[tuple[str, str]] = []

    # Método para manejar la acción de responder
    @rx.event
    async def answer(self):
        # Respuesta simulada (puedes reemplazarlo con lógica de IA o API)
        answer = f"Respuesta a: {self.question}"
        self.chat_history.append((self.question, answer))
        self.question = ""  # Limpia el input después de enviar la consulta
        yield

# Estilos comunes
shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
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

# Componente para cada mensaje de chat
def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(rx.text(question, style=question_style), text_align="right"),
        rx.box(rx.text(answer, style=answer_style), text_align="left"),
        margin_y="1em",
    )

# Historial de chat
def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        padding="1em",
        height="55vh",
        overflow_y="scroll",  # Habilita el scroll en caso de muchos mensajes
        border_radius="15px",
        bg=rx.color("gray", 1),
    )

# Barra de acciones para ingresar consultas
def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ingrese su consulta...",
            on_change=State.set_question,
            border_radius="40px",
            width="70%",
        ),
        rx.button(
            "Enviar",
            on_click=State.answer,
            margin_left="1em",
            border_radius="20px",
        ),
        width="100%",
        spacing="4",  # Espaciado válido en Reflex
        align="center",
        padding="1em",
    )

# Componente principal que contiene la UI del chatbot
def stackbot() -> rx.Component:
    return rx.stack(
        rx.container(
            rx.vstack(
                chat(),
                action_bar(),
                spacing="4",  # Espaciado válido entre chat y barra de acciones
            ),
            width="270px",
            height="70vh",
            padding="1em",
            bg="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/fondo_chatbot.jpg?raw=true') center/cover",
            border_radius="15px",
            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
        ),
        position="absolute",
        bottom="2%",
        right="10%",
    )
