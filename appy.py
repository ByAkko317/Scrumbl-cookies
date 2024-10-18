import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from api_handler import ApiRequestHandler

app = Flask(__name__)

# Cargar la API desde el archivo .env
load_dotenv()
API_KEY = os.getenv('API')

if API_KEY is None:
    raise RuntimeError("Error: No se encontró la clave API. Verifique su archivo .env.")

# Función para generar la URL del clima actual
def generar_url_ciudad(ciudad, pais, unidad):
    return f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&appid={API_KEY}&units={unidad}"

# Opción 1: Nueva consulta (implementada)
@app.route('/consulta/<ciudad>/<pais>')
def nueva_consulta(ciudad, pais):
    unidad_de_medida = "metric"  # Puede ser 'metric' o 'imperial'
    url_clima_actual = generar_url_ciudad(ciudad, pais, unidad_de_medida)
    
    # Crear instancia del manejador de API
    handler = ApiRequestHandler(url_clima_actual)
    
    # Intentar la solicitud
    resultado = handler.retry_request()
    
    if resultado["status"] == "success":
        return jsonify({"message": f"Clima en {ciudad}, {pais}", "data": resultado["data"]})
    else:
        return jsonify({"error": resultado["message"]}), 400

# Opción 2: Ver historial (aún no implementada)
@app.route('/historial')
def ver_historial():
    return jsonify({"message": "Esta funcionalidad estará disponible en la próxima entrega."})

# Opción 3: Cambiar unidades de medida (aún no implementada)
@app.route('/cambiar-unidades')
def cambiar_unidades():
    return jsonify({"message": "Esta funcionalidad estará disponible en la próxima entrega."})

# Opción 4: Salir
@app.route('/salir')
def salir():
    return jsonify({"message": "Gracias por usar la aplicación. ¡Adiós!"})

# Ruta principal: Menú principal
@app.route('/')
def index():
    return jsonify({
        "message": "Bienvenido al menú principal de la aplicación del clima.",
        "opciones": {
            "1": "Nueva Consulta (debe especificar ciudad y país en la URL: /consulta/<ciudad>/<pais>)",
            "2": "Ver Historial (próxima entrega)",
            "3": "Cambiar Unidades de Medida (próxima entrega)",
            "4": "Salir"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)

"""
Cambios realizados:
Separación de Concerns: El código ahora está estructurado en dos archivos para separar la lógica de la API del servidor Flask, facilitando su mantenimiento y escalabilidad.
Manejo de errores: El manejo de errores en la API ahora devuelve mensajes JSON en vez de imprimirlos en la consola. Esto es ideal para aplicaciones web, ya que el frontend 
puede mostrar estos errores de forma más amigable.
Menú interactivo por rutas: Las rutas de Flask devuelven las opciones del menú en formato JSON, en lugar de usar input() para recibir comandos.
Consulta del clima: La funcionalidad de "Nueva Consulta" ya está desarrollada y lista para enviar solicitudes a la API del clima. Solo requiere que la ciudad y 
el país se especifiquen en la URL (por ejemplo, /consulta/Londres/UK).
Este diseño está listo para ser conectado a una interfaz gráfica que hará solicitudes HTTP a las rutas definidas, permitiendo una experiencia más intuitiva para el usuario.

"""