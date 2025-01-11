import reflex as rx


rx.stack(
                        rx.container(
                            width="200px",
                            height="45vh",
                            center_content=True,
                            bg=rx.color("accent", 3),
                            border_radius="15px",
                            box_shadow="10px 10px 15px rgba(0, 0, 0, 0.3), 0px 0px 5px transparent",
                        ),
                        position="absolute",  # Posicionamiento absoluto
                        bottom="2%",  # Alineado al borde inferior
                        right="60%",  # Alineado al borde izquierdo
                    ),