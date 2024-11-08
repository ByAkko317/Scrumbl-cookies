from flask import Flask,render_template,request,flash,redirect,url_for
from dotenv import load_dotenv
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
import requests
import os
import re
import time

app=Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

unidad_de_medida = "metric"
símbolo_medida = { 
    "metric": "ºC",
    "imperial": "ºF"
}
def cargar_preferencia_unidades():
    global unidad_de_medida
    mensaje = ""
    try:
        with open("Preferencia.txt", "r") as archivo:
            unidad_de_medida = archivo.readline().strip()
            mensaje = f"Se ha cargado la preferencia de unidad: {unidad_de_medida}."
    except FileNotFoundError:
        mensaje = "No se encontró un archivo de preferencias. Se utilizará 'metric' como predeterminado."
        unidad_de_medida = "metric"
    return mensaje

class ApiRequestHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def make_request(self):
        try:
            response = requests.get(self.api_url, timeout=5)
            if 200 <= response.status_code < 300:
                return {"status": "success", "data": response.json()} 
            elif response.status_code == 400:
                return {"status": "error", "message": "Solicitud inválida, revise los datos ingresados."}
            elif response.status_code == 401:
                return {"status": "error", "message": "Autenticación fallida, verifique las credenciales."}
            elif response.status_code == 404:
                return {"status": "error", "message": "Datos no encontrados, verifique la información."}
            elif response.status_code == 500:
                return {"status": "error", "message": "Error en el servidor, intente más tarde."}
            elif 502 <= response.status_code <= 504:
                return {"status": "error", "message": "API no disponible, intente más tarde."}
            else:
                return {"status": "error", "message": f"Error inesperado: {response.status_code}"}
        except Timeout:
            return {"status": "error", "message": "La solicitud tardó demasiado. Verifique su conexión."}
        except ConnectionError:
            return {"status": "error", "message": "Error de conexión. Verifique su conexión a Internet."}
        except HTTPError as http_err:
            return {"status": "error", "message": f"Error HTTP: {http_err}"}
        except RequestException as req_err:
            return {"status": "error", "message": f"Error en la solicitud: {req_err}"}
        except Exception as err:
            return {"status": "error", "message": f"Ocurrió un error inesperado: {err}"}
    def retry_request(self, retries=3):
        for attempt in range(retries):
            result = self.make_request()
            if result["status"] == "success":
                return result
        return {"status": "error", "message": "Se agotaron los intentos. Intente más tarde."}

def guardar_en_historial(ciudad, pais, informacion):
    marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    consulta = f"Fecha y hora: {marca_tiempo}\nCiudad: {ciudad}, {pais}\n"
    consulta += f"Temperatura actual: {informacion['temp_actual']}{símbolo_medida[unidad_de_medida]}, "
    consulta += f"Temperatura máxima: {informacion['temp_max']}{símbolo_medida[unidad_de_medida]} y "
    consulta += f"Temperatura mínima: {informacion['temp_min']}{símbolo_medida[unidad_de_medida]}.\n"
    consulta += f"Condiciones climáticas: {informacion['clima']}, humedad: {informacion['humedad']}% .\n"
    consulta += f"Velocidad del viento: {informacion['viento_vel']} m/s, "
    consulta += f"Dirección del viento: {informacion['viento_dir']}° "
    
    if 'alerta' in informacion:
        consulta += f"Alerta meteorológica: {informacion['alerta']}\n"
    with open("Historial.txt", "a") as archivo:
        archivo.write(consulta)
        archivo.write("\n")

def validar_entrada(texto):
    solo_letras = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
    return solo_letras.match(texto) is not None

@app.route("/")
def home():
    mensaje_preferencia = cargar_preferencia_unidades()
    return render_template('index.html', mensaje_preferencia=mensaje_preferencia, simbolo=símbolo_medida[unidad_de_medida])

@app.route('/consulta_clima')
def consulta_clima():
    return render_template('obtenerCLima.html')

@app.route("/consulta_clima" , methods=['GET','POST'])
def obtener_clima():
    # Recibe los datos del formulario o de la url
    ciudad = request.args.get('ciudad') or request.form.get('ciudad', '').strip()
    pais = request.args.get('pais') or request.form.get('pais', '').strip()

    if ciudad and pais:
        load_dotenv()
        api=os.getenv('API')
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&lang=sp&appid={api}&units={unidad_de_medida}"
        
        api_handler = ApiRequestHandler(api_url)
        result = api_handler.retry_request()
        
        if result["status"] == "success":
            data = result["data"]
            weather_info = {
                "temperature": data.get("main", {}).get("temp"),
                "temp_max": data.get("main", {}).get("temp_max"),
                "temp_min": data.get("main", {}).get("temp_min"),
                "description": data.get("weather", [{}])[0].get("description"),
                "wind_speed": data.get("wind", {}).get("speed"),
                "wind_direction": data.get("wind", {}).get("deg", "No disponible"),
                "icon": data.get("weather",[{}])[0].get("icon"),
                "humidity":data.get("main",{}).get("humidity")
            }
            informacion = {
                "temp_actual": weather_info["temperature"],
                "temp_max": weather_info["temp_max"],
                "temp_min": weather_info["temp_min"],
                "clima": weather_info["description"],
                "viento_vel": weather_info["wind_speed"],
                "viento_dir": weather_info["wind_direction"],
                "humedad":weather_info ["humidity"]
            }
            if 'alerts' in data:
                informacion['alerta'] = data['alerts'][0]['description']
            guardar_en_historial(ciudad, pais, informacion)
            return render_template('resultado.html', ciudad=ciudad, pais=pais, weather_info=weather_info, unidad=símbolo_medida[unidad_de_medida])
        elif result["status"] == "error":
            flash(result["message"])
            return redirect(url_for('consulta_clima'))
        else:
            return flash(msg="ERROR \nNo se pudo obtener la información del clima.")
    else:
        return render_template('consulta_clima.html', ciudad=ciudad, pais=pais)

@app.route('/consulta_pronostico')
def consulta_pronóstico():
    return render_template('obtener_pronostico.html')

@app.route("/consulta_pronostico", methods=['POST'])
def obtener_pronóstico():
    load_dotenv()
    api=os.getenv('API')
    ciudad = request.form.get('ciudad')
    pais = request.form.get('pais')
    if not validar_entrada(ciudad) or not validar_entrada(pais):
        flash("Por favor, ingrese solo letras en ambos campos.")
        return redirect(url_for('consulta_pronostico'))
    
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad},{pais}&cnt=40&lang=sp&appid={api}&units={unidad_de_medida}"
    
    api_handler = ApiRequestHandler(api_url)
    result = api_handler.retry_request()
    pronosticos_por_dia = {}
    resumen_datos = {}
    
    if result["status"] == "success":
        data = result["data"]
        for item in data['list']:
            fecha = item['dt_txt'].split(" ")[0]
            hora = item['dt_txt'].split(" ")[1]
            if hora == "12:00:00":
                pronosticos_por_dia[fecha] = {
                    "clima": item['weather'][0]['description'],
                    "temp": item['main']['temp'],
                    "temp_max": item['main']['temp_max'],
                    "temp_min": item['main']['temp_min'],
                    "fenomenos": item['weather'][0]['main'],
                    "viento_velocidad": item['wind']['speed'],
                    "viento_direccion": item['wind'].get('deg', 'No disponible'),
                    "humedad": item['main'].get('humidity'),
                    "icon": item['weather'][0]['icon']
                }
                if fecha not in resumen_datos:
                    resumen_datos[fecha] = {"temp": [], "humedad": [], "climas": []}
                    resumen_datos[fecha]["temp"].append(item['main']['temp'])
                    resumen_datos[fecha]["humedad"].append(item['main'].get('humidity', 0))
                    resumen_datos[fecha]["climas"].append(item['weather'][0]['main'])
        for fecha, item in pronosticos_por_dia.items():
            clima = item['clima']
            temperatura = item['temp']
            temp_max = item['temp_max']
            temp_min = item['temp_min']
            humedad = item['humedad']  
            fenomenos = item['fenomenos']
            wind_vel= item['viento_velocidad']
            wind_dir=item['viento_direccion']
            humedad=item['humedad']
            alerta = ""
            if fenomenos in ['Rain', 'Thunderstorm', 'Snow']:
                alerta = f"¡Atención! Se esperan {fenomenos.lower()}."
                item['alerta'] = alerta
            informacion = {
                    "temp_actual": temperatura,
                    "temp_max": temp_max,
                    "temp_min": temp_min,
                    "clima": clima,
                    "viento_vel": wind_vel,
                    "viento_dir": wind_dir,
                    "humedad": humedad
                }
            if 'alerts' in data:
                informacion['alerta'] = data['alerts'][0]['description']
            guardar_en_historial(ciudad, pais, informacion)
        resumen_promedios = {}
        for fecha, datos in resumen_datos.items():
            promedio_temp = sum(datos["temp"]) / len(datos["temp"])
            promedio_humedad = sum(datos["humedad"]) / len(datos["humedad"])
            clima_frecuente = max(set(datos["climas"]), key=datos["climas"].count)
            resumen_promedios[fecha] = {
                "temp_promedio": promedio_temp,
                "humedad_promedio": promedio_humedad,
                "clima_frecuente": clima_frecuente
            }
    elif result["status"] == "error":
        flash(result["message"])
        return redirect(url_for('consulta_clima'))
    else:
        flash("Error al obtener el pronóstico. Intente de nuevo más tarde.")
        return redirect(url_for('consulta_pronostico'))
    return render_template('resultado.html', ciudad=ciudad,pais=pais,pronosticos=pronosticos_por_dia, resumen=resumen_promedios,unidad=símbolo_medida[unidad_de_medida])
    #cuando se pasan los datos en render_template, la primer variable corresponde a una variable declarada en html, y la segunda en python

@app.route('/consulta_desde_historial/<ciudad>/<pais>', methods=['GET'])
def consulta_desde_historial(ciudad, pais):
    return render_template('obtenerClima.html', ciudad=ciudad, pais=pais)

@app.route('/historial')
def ver_historial():
    consultas = []
    try:
        with open("Historial.txt", "r") as archivo:
            entrada = {}
            for linea in archivo:
                if linea.startswith("Fecha y hora:"):
                    if entrada:
                        consultas.append(entrada)  
                    entrada = {"fecha_hora": linea.strip().split(": ", 1)[1]}
                elif linea.startswith("Ciudad:"):
                    ciudad_pais = linea.strip().split(": ", 1)[1].split(", ")
                    entrada["ciudad"] = ciudad_pais[0]
                    entrada["pais"] = ciudad_pais[1]
                else:
                    entrada["detalles"] = entrada.get("detalles", "") + linea
            if entrada:
                consultas.append(entrada)
    except FileNotFoundError:
        flash("El archivo de historial no existe aún. No se han registrado consultas.")
    
    for consulta in consultas:
        if 'ciudad' not in consulta or 'pais' not in consulta:
            flash("Una de las entradas no tiene los datos necesarios para realizar una nueva consulta.")
            continue
    return render_template('ver_historial.html', consultas=consultas)

@app.route('/borrar_historial', methods=['POST'])
def borrar_historial():
    with open("Historial.txt", "w") as archivo:
        archivo.write("")
    flash("El historial ha sido borrado correctamente.")
    return redirect(url_for('ver_historial'))

@app.route('/cambiar_unidades', methods=['GET', 'POST'])
def cambiar_unidades():
    global unidad_de_medida
    unidad_actual = 'Celsius' if unidad_de_medida == 'metric' else 'Imperial'
    
    if request.method == 'POST':
        seleccion = request.form.get("unidad")
        
        if seleccion == 'metric':
            if unidad_de_medida != 'metric':
                unidad_de_medida = 'metric'
                flash("Unidad de medida cambiada a Celsius.")
        elif seleccion == 'imperial':
            if unidad_de_medida != 'imperial':
                unidad_de_medida = 'imperial'
                flash("Unidad de medida cambiada a Fahrenheit.")
        with open("Preferencia.txt", "w") as archivo:
            archivo.write(unidad_de_medida)
        return redirect(url_for('cambiar_unidades'))
    return render_template("cambiar_unidades.html", unidad_actual=unidad_actual, simbolo=símbolo_medida[unidad_de_medida])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)