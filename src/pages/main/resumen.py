import reflex as rx
from rxconfig import config
from .modulos import header, sidebar_bottom_profile, pop_up_message, SidebarState
from .bot_interface import stackbot
from whoosh.qparser import QueryParser
from .modulos import ix  # Importa el índice desde modulos.py

# Estado de la página resumen
class ResumenState(rx.State):
    search_results: list[str] = []  # Almacenar resultados

    @rx.event
    def load_results(self):
        """Carga los resultados de búsqueda en base al término ingresado."""
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(SidebarState.search_query.lower())
            results = searcher.search(query)
            self.search_results = [result["content"] for result in results]

# Componente de la página resumen
def resumen_page() -> rx.Component:
    return rx.vstack(
        rx.text("Resultados de la búsqueda", size="3", weight="bold", margin_bottom="1em"),
        rx.foreach(ResumenState.search_results, lambda result: rx.box(
            rx.text(result, size="9"), padding="1em", border="1px solid #ddd", margin_bottom="0.5em"
        )),
        padding="2em",
    )

def resumen() -> rx.Component:
    """Página Resumen."""
    return rx.box(
        header(),  # Llamamos a la función del encabezado aquí
        rx.hstack(
            rx.container(
                rx.vstack(
                    rx.heading(
                        rx.fragment(
                            rx.text("Resumen de la búsqueda"),
                        ),
                        size="6"
                    ),
                    resumen_page(),
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
            stackbot(),
            sidebar_bottom_profile(),
            pop_up_message(),  # login_multiple_thirdparty() puede reemplazar esto si es necesario
            spacing="4",  # Ajusta el espaciado entre el contenido
            align="start",  # Alinea el contenido al inicio
        ),
        min_height="100vh",
        width="100vw",
        background="url('https://github.com/arnaldoquinones/bot_de_prueba/blob/master/src/pages/assets/circuito_fondo.png?raw=true')",
        background_size="cover",  # Ajusta el tamaño de la imagen para cubrir todo el fondo
        background_repeat="no-repeat",  # Evita que la imagen se repita
        background_position="center",  # Centra la imagen en el fondo
        overflow_y="auto",
    )
