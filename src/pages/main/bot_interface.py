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
    max_height="auto",
)

answer_style = message_style | dict(
    margin_right="5%",
    background_image="linear-gradient(to right, #8e44ad, #e91e63, #3498db)",
    max_height="auto",
    position="relative", 
    z_index="2"  # Higher z-index to overlap dots
)

# answer_style = {
#     "background": "linear-gradient(to right, #8e44ad, #e91e63, #3498db)",  # Gradiente de colores
#     "border-radius": "20px",  # Bordes redondeados
#     "padding": "5px 10px",  # Reducir el padding
#     "line-height": "1.2",  # Ajustar el line-height
#     "max-width": "80%",  # Tamaño máximo de la burbuja
#     "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",  # Sombra
#     "position": "relative",  # Para la punta de la burbuja
# }

# question_style = {
#     "background": "linear-gradient(to right, #0e8174, #08354b)",  # Gradiente de colores
#     "border-radius": "20px",  # Bordes redondeados
#     "padding": "5px 10px",  # Reducir el padding
#     "line-height": "1.2",  # Ajustar el line-height
#     "max-width": "80%",  # Tamaño máximo de la burbuja
#     "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",  # Sombra
#     "position": "relative",  # Para la punta de la burbuja
# }

def qa(question: str, answer: str) -> rx.Component:
    """Renderiza un par de pregunta-respuesta."""
    return rx.box(
        rx.box(rx.text(question, style=question_style), text_align="right"),
        rx.box(rx.text(answer, style=answer_style), text_align="left"),
        margin_y="0.8em",
        width="100%",
    )

style = {
    "animate": {
        "@keyframes spin": {
            "0%": {
                "transform": "rotate(0deg)"
            },
            "100%": {
                "transform": "rotate(-360deg)"  # Rotación en sentido inverso
            }
        },
        "@keyframes bounce": {  # Ajustar la altura del rebote
            "0%, 80%, 100%": {
                "transform": "translateY(0)"
            },
            "40%": {
                "transform": "translateY(-10px)"  # Rebote más bajo
            }
        }
    }
}

def dots_component():
    return rx.box(
        rx.hstack(
            rx.box(
                width="7px",
                height="7px",
                border_radius="50%",
                bg="white",
                animation="bounce 1.5s infinite ease-in-out",
                animation_delay="0s",  # Primer punto
            ),
            rx.box(
                width="7px",
                height="7px",
                border_radius="50%",
                bg="white",
                animation="bounce 1.5s infinite ease-in-out",
                animation_delay="0.3s",  # Segundo punto
            ),
            rx.box(
                width="7px",
                height="7px",
                border_radius="50%",
                bg="white",
                animation="bounce 1.5s infinite ease-in-out",
                animation_delay="0.6s",  # Tercer punto
            ),
            spacing="2",
            align="center",
            justify="center",
            ),
            position="absolute",
            z_index="1", # Lower z-index
    )

def modulo():
    return rx.stack(
        rx.box(
            rx.box(
                
                width="calc(100% - 2px)",
                height="calc(100% - 2px)",
                border_radius="1rem",
                background="linear-gradient(to bottom, rgb(30, 41, 59), rgb(15, 23, 42))",
                position="absolute",
                left="1px",
                top="1px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            width="277px", 
            height="55.5vh",
            position="relative",
            overflow="hidden",
            border_radius="1rem",
            background="linear-gradient(to bottom, rgb(51, 65, 85), rgb(30, 41, 59))",
            _before={
                "content": "''",
                "position": "absolute",
                "left": "-100%",
                "top": "-100%",
                "height": "300%",
                "width": "300%",
                "background": "conic-gradient(rgba(0, 182, 255, 0.6) 0deg, rgba(0, 132, 252, 0.6) 120deg, transparent 240deg)",
                "animation": "spin 5s linear infinite",
                "border-radius": "1rem",
            },
            style=style["animate"]
        ),
        position="absolute",
        bottom="10%",
        right="60%",
    )

# Initialize app with styles
app = rx.App(style=style)

def chat() -> rx.Component:
    """Área de chat."""
    return rx.box(
        rx.box(dots_component(),
        position="absolute",  # Utilizamos "absolute" para moverlo
        top="82%",  # 10% desde la parte superior de la pantalla
        left="20%"),  # 10% desde la parte izquierda de la pantalla
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
            display="flex",  # Add flex display.
            flex_direction="column",  # Reverse the direction.
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