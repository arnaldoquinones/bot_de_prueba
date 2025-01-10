from user_agents import parse
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def detect_device():
    # Obtiene el User-Agent desde la solicitud
    user_agent = request.headers.get("User-Agent")
    if not user_agent:
        return "No se pudo detectar el User-Agent."

    # Analiza el User-Agent
    parsed_user_agent = parse(user_agent)

    # Clasifica el dispositivo
    if parsed_user_agent.is_mobile:
        device_type = "Mobile"
    elif parsed_user_agent.is_tablet:
        device_type = "Tablet"
    else:
        device_type = "PC/Desktop"

    return f"Estás navegando desde un {device_type}."

if __name__ == "__main__":
    app.run(debug=True)









from user_agents import parse

# Ejemplo de User-Agent (puedes reemplazarlo con el real)
user_agent = "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36"

# Analiza el User-Agent
parsed_user_agent = parse(user_agent)

if parsed_user_agent.is_mobile:
    # Código adaptado para dispositivos móviles
    print("Estás navegando desde un dispositivo móvil.")
    # Por ejemplo, mostrar un diseño más compacto
    mobile_ui()

elif parsed_user_agent.is_tablet:
    # Código adaptado para tablets
    print("Estás navegando desde una tablet.")
    # Por ejemplo, un diseño optimizado para pantallas intermedias
    tablet_ui()

else:
    # Código adaptado para PC o Desktop
    print("Estás navegando desde una PC o Desktop.")
    # Por ejemplo, un diseño con más espacio y funcionalidad avanzada
    desktop_ui()

# Funciones de ejemplo
def mobile_ui():
    print("Cargando diseño compacto para móviles.")

def tablet_ui():
    print("Cargando diseño adaptado para tablets.")

def desktop_ui():
    print("Cargando diseño completo para desktops.")
