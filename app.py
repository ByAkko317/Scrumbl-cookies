from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from clima import obtener_clima
from clima import obtener_pronostico
from clima import ver_historial, borrar_historial
from clima import cambiar_unidades

app = Flask(__name__)
app.run(host='0.0.0.0', port=5500)
@app.route('/obtener_clima', methods=['POST'])
def obtener_clima_route():
    datos = request.get_json()
    nombre_ciudad = datos.get('nombre_ciudad')
    nombre_pais = datos.get('nombre_pais')
    if nombre_ciudad and nombre_pais:
        resultado = obtener_clima(nombre_ciudad, nombre_pais)
        return jsonify({'resultado': resultado})
    return jsonify({'error': 'Faltan parámetros'}), 400

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/obtener_pronostico', methods=['POST'])
def obtener_pronostico_route():
    datos = request.get_json()
    nombre_ciudad = datos.get('nombre_ciudad')
    nombre_pais = datos.get('nombre_pais')
    if nombre_ciudad and nombre_pais:
        resultado = obtener_pronostico(nombre_ciudad, nombre_pais)
        return jsonify({'resultado': resultado})
    return jsonify({'error': 'Faltan parámetros'}), 400

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ver_historial', methods=['GET'])
def ver_historial_route():
    resultado = ver_historial()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/cambiar_unidades', methods=['POST'])
def cambiar_unidades_route():
    datos = request.get_json()
    seleccion = datos.get('seleccion')
    resultado = cambiar_unidades(seleccion)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(debug=True)
