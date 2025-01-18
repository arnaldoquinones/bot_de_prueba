import reflex as rx


class State(rx.State):
    question: str = ""
    chat_history: list[tuple[str, str]] = []
    window_open: bool = False  # Controla si la ventana está abierta

    def submit_message(self):
        """Procesar el mensaje del usuario."""
        if self.question.strip():
            answer = f"Respuesta a: {self.question}"
            self.chat_history.append((self.question, answer))
            self.question = ""
            # Forzar scroll al fondo después de enviar mensaje
            return rx.call_script("scrollToBottom()")

   
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

    @rx.event
    def set_question(self, value: str):
        """Handle text input with auto line breaks."""
        # Insert line break every 30 characters
        chunks = [value[i:i+25] for i in range(0, len(value), 25)]
        self.question = '\n'.join(chunks)
    
# Estilo minimalista para la barra de desplazamiento
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
            "background-color": rx.color("gray", 5),  # Un poco más oscuro al hover
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
    background="linear-gradient(to right, #0e8174, #08354b)",
)

answer_style = message_style | dict(
    margin_right="5%",
    background_image="linear-gradient(to right, #8e44ad, #e91e63, #3498db)",
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
             # Add spacer div at top
            rx.box(height="40vh"),  # This pushes first message down
            rx.foreach(
                State.chat_history,
                lambda messages: qa(messages[0], messages[1]),
            ),
            width="100%",
            height="100%",
            overflow_y="auto",
            style=scrollbar_style,
            id="chat-container",
            display="flex",  # Add flex display
            flex_direction="column",  # Reverse the direction
            on_mount=rx.call_script("""
                function scrollToBottom() {
                    const container = document.getElementById('chat-container');
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    }
                }
                scrollToBottom();
                const observer = new MutationObserver(scrollToBottom);
                observer.observe(document.getElementById('chat-container'), { 
                    childList: true, 
                    subtree: true 
                });
            """),
        ),
        padding="0.8em",
        height="55vh",
        border_radius="12px",
        bg="rgba(200, 200, 200, 0.1)",  # Gris claro con 10% de opacidad
        backdrop_filter="blur(6px)",  # Efecto de difuminado suave
        margin_bottom="0.5em",
        margin_top="20px",
        width="100%",
        box_shadow="0px 4px 8px rgba(0, 0, 0, 0.1)",  # Sombra sutil para resaltar el contenedor
    )

def action_bar() -> rx.Component:
    return rx.vstack(
        rx.input(
            value=State.question,
            placeholder="Ingrese su consulta...",
            on_change=State.set_question,
            on_key_down=State.handle_key_down,
            border_radius="40px",
            width="88%",
            margin_top="-15px",  # Increased negative margin to move up
            max_length=120,
            rows="1",
            resize="none",
            border="none !important",  # Force remove border
            outline="none !important", # Force remove outline
            style={
                "overflow-y": "auto",
                "word-wrap": "break-word",
                "padding": "6px 12px",
                "line-height": "1.1",
                "min-height": "28px",
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
                }
            },
        ),
        rx.icon(
            tag="send-horizontal",
            margin_right="2%",
            margin_top="-40px",  # Adjusted for new textarea position
            align_self="flex-end",
            size=22,
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


# Sidebar con el botón para abrir el chatbot, ahora posicionado abajo
def sidebar() -> rx.Component:
    return rx.box(
        rx.button(
            "Abrir Chatbot",
            on_click=State.toggle_window,
            bg="blue.500",  # Color de fondo del botón
            color="white",  # Color del texto
            padding="10px 20px",  # Padding del botón
            border_radius="20px",  # Bordes redondeados
            _hover={"bg": "blue.600"},  # Color al pasar el mouse
        ),
        position="fixed",
        left="20px",  # Margen desde la izquierda
        bottom="20px",  # Posicionado desde abajo
        z_index="1000",  # Asegura que esté por encima de otros elementos
    )

def main_layout() -> rx.Component:
    """Diseño principal con sidebar y chatbot."""
    return rx.box(
        sidebar(),
        stackbot(),
    )

