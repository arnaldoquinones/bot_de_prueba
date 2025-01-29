import reflex as rx
import asyncio
from typing import List, Tuple

class State(rx.State):
    question: str = ""
    chat_history: List[Tuple[str, str]] = []
    window_open: bool = False
    show_loading_dots: bool = False
    is_processing: bool = False

    @rx.event
    async def answer(self):
        """Maneja el retraso y añade la respuesta al chat."""
        if self.question.strip() and not self.is_processing:
            self.is_processing = True
            
            # 1. Añadir pregunta inmediatamente
            user_question = self.question
            self.chat_history.append((user_question, ""))  # Respuesta vacía temporal
            self.show_loading_dots = True
            self.question = ""
            yield  # Actualizar UI
            
            # 2. Esperar 2 segundos
            await asyncio.sleep(2)
            
            # 3. Reemplazar respuesta vacía con la real
            answer = f"Respuesta a: {user_question}"
            self.chat_history[-1] = (user_question, answer)
            self.show_loading_dots = False
            self.is_processing = False
            yield
            
            # Scroll al fondo
            yield rx.call_script(
                "document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;"
            )

    @rx.event
    async def handle_key_down(self, key: str):
        if key == "Enter" and not self.is_processing:
            yield State.answer
        yield

    @rx.event
    def toggle_window(self):
        """Alternar visibilidad de la ventana."""
        self.window_open = not self.window_open

    @rx.event
    def set_question(self, value: str):
        """Formatea el texto con saltos de línea."""
        chunks = [value[i:i+25] for i in range(0, len(value), 25)]
        self.question = '\n'.join(chunks)

# =====================================
# ESTILOS Y COMPONENTES (ORIGINALES)
# =====================================
scrollbar_style = {
    "&::-webkit-scrollbar": {"width": "6px"},
    "&::-webkit-scrollbar-thumb": {
        "background-color": "rgba(255, 255, 255, 0.1)",
        "border-radius": "3px",
    },
    "&::-webkit-scrollbar-track": {"background": "transparent"},
    "scrollbar-width": "thin",
    "scrollbar-color": f"{rx.color('gray', 4)} transparent",
    "&:hover": {
        "&::-webkit-scrollbar-thumb": {
            "background-color": rx.color("gray", 5),
        }
    },
}

message_style = dict(
    padding="0.8em",
    margin_y="0.4em",
    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
    max_width="90%",
    display="inline-block",
)

question_style = message_style | dict(
    margin_left="5%",     
    background="linear-gradient(to left, #0e8174, #08354b)",
    border_radius="30px 20px 1px 30px",
    max_width="70%",  # Limita el ancho máximo
    overflow="hidden",  # Maneja el desbordamiento
    word_wrap="break-word",  # Asegura que el texto se ajuste
    position="relative",
    z_index="1"
)

answer_style = message_style | dict(
    margin_right="5%",
    background_image="linear-gradient(to right, #8e44ad, #e91e63, #3498db)",
    border_radius="1px 30px 30px 20px",
    max_width="70%",  # Limita el ancho máximo
    overflow="hidden",  # Maneja el desbordamiento
    word_wrap="break-word",  # Asegura que el texto se ajuste
    position="relative",
    z_index="2"
)

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.vstack(  # Cambiado a vstack para mejor control vertical
            rx.box(
                rx.text(question, style=question_style),
                text_align="right",
                width="100%",
                padding_y="0.5em"  # Espacio vertical consistente
            ),
            rx.cond(
                answer != "",
                rx.box(
                    rx.text(answer, style=answer_style),
                    text_align="left",
                    width="100%",
                    padding_y="0.5em"  # Espacio vertical consistente
                ),
                rx.box(height="0.8em")
            ),
        ),
        spacing="1em",  # Espacio entre elementos del vstack
        width="100%",
        align_items="stretch"  # Asegura que los elementos se estiren apropiadamente
    )



style = {
    "animate": {
        "@keyframes spin": {
            "0%": {"transform": "rotate(0deg)"},
            "100%": {"transform": "rotate(-360deg)"}
        },
        "@keyframes bounce": {
            "0%, 80%, 100%": {"transform": "translateY(0)"},
            "40%": {"transform": "translateY(-10px)"}
        }
    }
}

def dots_component():
    return rx.cond(
        State.show_loading_dots,
        rx.hstack(
            rx.box(width="7px", height="7px", border_radius="50%", bg="white",
                   animation="bounce 1.5s infinite ease-in-out", animation_delay="0s"),
            rx.box(width="7px", height="7px", border_radius="50%", bg="white",
                   animation="bounce 1.5s infinite ease-in-out", animation_delay="0.3s"),
            rx.box(width="7px", height="7px", border_radius="50%", bg="white",
                   animation="bounce 1.5s infinite ease-in-out", animation_delay="0.6s"),
            spacing="2", align="center", justify="center",
        ),
    )

def modulo():
    return rx.stack(
        rx.box(
            rx.box(
                width="calc(100% - 2px)", height="calc(100% - 2px)",
                border_radius="1rem",
                background="linear-gradient(to bottom, rgb(30, 41, 59), rgb(15, 23, 42))",
                position="absolute", left="1px", top="1px",
                display="flex", align_items="center", justify_content="center",
            ),
            width="277px", height="55.5vh",
            position="relative", overflow="hidden", border_radius="1rem",
            background="linear-gradient(to bottom, rgb(51, 65, 85), rgb(30, 41, 59))",
            _before={
                "content": "''",
                "position": "absolute",
                "left": "-100%", "top": "-100%",
                "height": "300%", "width": "300%",
                "background": "conic-gradient(rgba(0, 182, 255, 0.6) 0deg, rgba(0, 132, 252, 0.6) 120deg, transparent 240deg)",
                "animation": "spin 5s linear infinite",
                "border-radius": "1rem",
            },
            style=style["animate"]
        ),
        position="absolute", bottom="10%", right="60%",
    )


app = rx.App(style=style)

def chat() -> rx.Component:
    return rx.box(
        rx.box(
            dots_component(),
            position="absolute",
            top="85%",
            left="12%",
        ),
        rx.box(
            rx.box(height="40vh"),
            rx.foreach(State.chat_history, lambda messages: qa(messages[0], messages[1])),
            width="100%", 
            height="100%", 
            overflow_y="auto",
            style=scrollbar_style, 
            id="chat-container",
            display="flex", 
            flex_direction="column",
            padding_top="-1cm",  # <-- Ajuste aquí
            on_mount=rx.call_script("""
                function scrollToBottom() {
                    const container = document.getElementById('chat-container');
                    if (container) container.scrollTop = container.scrollHeight;
                }
                scrollToBottom();
                const observer = new MutationObserver(scrollToBottom);
                observer.observe(document.getElementById('chat-container'), { 
                    childList: true, subtree: true 
                });
            """),
        ),
        padding="0.8em", 
        height="55vh", 
        border_radius="12px",
        bg="rgba(200, 200, 200, 0.1)", 
        backdrop_filter="blur(6px)",
        margin_bottom="0.5em", 
        margin_top="20px", 
        width="100%",
        box_shadow="0px 4px 8px rgba(0, 0, 0, 0.1)",
    )


def action_bar() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.heading(
                "Chatbot",
                size="4",
                color="white",
                align="center",
                margin_top="-2em",
                position="relative",
                top="-19.5em"
            ),
            width="100%"
        ),
        rx.input(
            value=State.question,
            placeholder="Ingrese su consulta...",
            on_change=State.set_question,
            on_key_down=State.handle_key_down,
            border_radius="40px",
            position="relative",
            top="-1em",
            left="-6%",  # Ajusta este valor según necesites
            width="88%",
            margin_top="-12px",  # Increased negative margin to move up
            max_length=120,
            rows="1",
            resize="none",
            border="none !important",  # Force remove border
            outline="none !important",  # Force remove outline
            style={
                "overflow-y": "auto",
                "word-wrap": "break-word",
                "padding": "6px 12px",
                "line-height": "1.1",
                "min-height": "25px",
                "max-height": "50px",
                "width": "90%",
                "box-sizing": "border-box",
                "white-space": "pre-wrap",
                "word-break": "break-word",
                "font-size": "14px",
                "border": "none !important",
                "outline": "none !important",
                "background-color": "rgba(255, 255, 255, 0.1)",
                "_focus": {
                    "border": "none !important",
                    "outline": "none !important",
                    "box-shadow": "none",
                },
                "_hover": {
                    "border": "none !important",
                    "outline": "none !important",
                },
            },
        ),
        rx.icon(
            tag="send-horizontal",
            margin_right="2%",
            margin_top="-52px",  # Adjusted for new textarea position
            align_self="flex-end",
            size=22,
            cursor="pointer",
            on_click=State.answer,
        ),
        spacing="3",
        align_items="center",
        justify_content="center",
        width="100%",
    )

def stackbot() -> rx.Component:
    """Ventana del chatbot."""
    return rx.stack(
        rx.container(
            rx.vstack(
                rx.vstack(
                modulo(),
                position="relative",  # Permite moverlo sin afectar a los demás elementos
                    top="363px",  # Desplaza hacia abajo
                    left="275px",  # Desplaza hacia la derecha
                ),
                chat(),
                action_bar(),
                top="6px",
                right="10px",
                spacing="3",
                width="100%",
            ),
            width="300px",
            height="70vh",
            padding="0.8em",
            background_color="rgba(0,0,0,0.6)",  # Más opaco
            backdrop_filter="blur(8px)",  # Más desenfoque
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
                top="6px",
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



def main_layout() -> rx.Component:
    """Diseño principal con sidebar y chatbot."""
    return rx.box(
        # sidebar(),
        stackbot(),
    )