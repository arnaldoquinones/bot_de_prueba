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
