import reflex as rx

class State(rx.State):
    question: str = ""
    chat_history: list[tuple[str, str]] = []

    def submit_message(self):
        """Procesa el mensaje al enviarlo."""
        if self.question.strip():
            answer = f"Respuesta a: {self.question}"
            self.chat_history.append((self.question, answer))
            self.question = ""  # Limpia la entrada después de enviar

    @rx.event
    async def answer(self):
        self.submit_message()
        yield

    @rx.event
    async def handle_key_down(self, key: str):
        if key == "Enter":
            self.submit_message()
        yield

shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "5%"
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
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        padding="0.8em",
        height="50vh",
        overflow_y="scroll",
        border_radius="12px",
        bg=rx.color("gray", 1),
        margin_bottom="0.5em",
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
            margin_right="2%",
            margin_top="48px",
            max_length=120,  # Límite absoluto de caracteres
        ),
        rx.icon(
            tag="send-horizontal",
            margin_right="2%",
            margin_top="-38px",
            align_self="flex-end",
            size=19,
            cursor="pointer",
        ),
        width="100%",
        on_click=State.answer,
    )

def stackbot() -> rx.Component:
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
        ),
        position="absolute",
        bottom="2%",
        right="40%",
    )
