import reflex as rx
import asyncio

# class State(rx.State):
#     """The main application state."""
#     landingpage_text: str = ""

#     async def landingpage_update(self):
#         """Simulación de efecto de texto con animación de tipo escritura."""
#         base_text = "Discover my "
#         services = ["Music", "Poems", "Art", "Pictures"]
#         while True:
#             for service in services:
#                 self.landingpage_text = base_text
#                 for char in service:
#                     await asyncio.sleep(0.2)
#                     self.landingpage_text += char
#                 await asyncio.sleep(1)
#                 for _ in range(len(service)):
#                     await asyncio.sleep(0.1)
#                     self.landingpage_text = self.landingpage_text[:-1]

#     async def on_load(self):
#         """Inicia el efecto de escritura automáticamente al cargar la página."""
#         await self.landingpage_update()



# def headerstyles():
#     """Estilos CSS personalizados en Reflex."""
#     return rx.style(
#         """
#         @keyframes fadeIn {
#           from {
#             opacity: 0;
#           }
#           to {
#             opacity: 1;
#           }
#         }

#         .fade-in-text {
#           animation: fadeIn 3s ease-in-out forwards;
#         }
#         """
#     )

