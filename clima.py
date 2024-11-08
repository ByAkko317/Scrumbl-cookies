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
<<<<<<< HEAD
    consulta += f"Temperatura actual: {informacion['temp_actual']}°C, "
    consulta += f"Temperatura máxima: {informacion['temp_max']}°C, "
    consulta += f"Temperatura mínima: {informacion['temp_min']}°C\n"
    consulta += f"Condiciones climáticas: {informacion['clima']}\n"
    consulta += f"Velocidad del viento: {informacion['viento_vel']} m/s, "
    consulta += f"Dirección del viento: {informacion['viento_dir']}°\n"
    consulta += f"Humedad: {informacion['humedad']}%"

    if 'alerta' in informacion:
        consulta += f"Alerta meteorológica: {informacion['alerta']}\n"
    consulta += "\n------------------------\n"  # Separador para cada consulta

    # Guardar en el archivo
=======
    consulta += f"Temperatura actual: {informacion['temp_actual']}{símbolo_medida[unidad_de_medida]}, "
    consulta += f"Temperatura máxima: {informacion['temp_max']}{símbolo_medida[unidad_de_medida]} y "
    consulta += f"Temperatura mínima: {informacion['temp_min']}{símbolo_medida[unidad_de_medida]}.\n"
    consulta += f"Condiciones climáticas: {informacion['clima']}, humedad: {informacion['humedad']}% .\n"
    consulta += f"Velocidad del viento: {informacion['viento_vel']} m/s, "
    consulta += f"Dirección del viento: {informacion['viento_dir']}° "
    
    if 'alerta' in informacion:
        consulta += f"Alerta meteorológica: {informacion['alerta']}\n"
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6
    with open("Historial.txt", "a") as archivo:
        archivo.write(consulta)
        archivo.write("\n")

def obtener_ultimas_consultas():
    try:
        with open("Historial.txt", "r") as archivo:
            lineas = archivo.readlines()
            consultas = []
            consulta_actual = []
            for linea in lineas:
                consulta_actual.append(linea)
                if "------------------------" in linea:
                    consultas.append(consulta_actual)
                    consulta_actual = []
            return consultas[-5:]  # Devuelve las últimas 5 consultas completas
    except FileNotFoundError:
        return []

def obtener_clima(nombre_ciudad, nombre_pais):
    load_dotenv()#obtención de datos de .env
    api = os.getenv('API')
    global unidad_de_medida
    url = f"https://api.openweathermap.org/data/2.5/weather?q={nombre_ciudad},{nombre_pais}&lang=sp&appid={api}&units={unidad_de_medida}"

@app.route("/")
def home():
    mensaje_preferencia = cargar_preferencia_unidades()
    return render_template('index.html', mensaje_preferencia=mensaje_preferencia, simbolo=símbolo_medida[unidad_de_medida])

<<<<<<< HEAD
    if result["status"] == "success":
        data = result["data"]#navegación dentro del JSON obtenido en formato diccionario, utilizando slicing
        clima = data['weather'][0]['description']
        temperatura = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        humedad = data['main'].get('humidity', 'No disponible')
        viento_velocidad = data['wind']['speed']  # Extraer la velocidad del viento
        viento_direccion = data['wind'].get('deg', 'No disponible')  # Extraer dirección si está disponible
        # Mensaje de notificación con los datos pertinentes
        print(f"\nEl clima en {nombre_ciudad}, {nombre_pais} es: {clima} con una temperatura de {temperatura} {símbolo_medida[unidad_de_medida]}.")
        print(f"Temperatura máxima: {temp_max}{símbolo_medida[unidad_de_medida]}, Temperatura mínima: {temp_min}{símbolo_medida[unidad_de_medida]}.")
        print(f"Humedad: {humedad}%") 
        print(f"Velocidad del viento: {viento_velocidad} m/s, Dirección: {viento_direccion}°.")
        

        # Preparar información para guardar en el historial
        informacion = {
            "temp_actual": temperatura,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "clima": clima,
            "humedad": humedad,
            "viento_vel": viento_velocidad,
            "viento_dir": viento_direccion
        }
=======
@app.route('/consulta_clima')
def consulta_clima():
    return render_template('obtenerCLima.html')

@app.route("/consulta_clima" , methods=['GET','POST'])
def obtener_clima():
    # Recibe los datos del formulario o de la url
    ciudad = request.args.get('ciudad') or request.form.get('ciudad', '').strip()
    pais = request.args.get('pais') or request.form.get('pais', '').strip()
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6

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
<<<<<<< HEAD
                    "humedad": item['main']['humidity'],
                    "fenomenos": item['weather'][0]['main'], # Fenómenos meteorológicos
                    "viento_velocidad" : item['wind']['speed'],  # Velocidad del viento
                    "viento_direccion" : item['wind'].get('deg', 'No disponible')  # Dirección del viento si está disponible
=======
                    "fenomenos": item['weather'][0]['main'],
                    "viento_velocidad": item['wind']['speed'],
                    "viento_direccion": item['wind'].get('deg', 'No disponible'),
                    "humedad": item['main'].get('humidity'),
                    "icon": item['weather'][0]['icon']
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6
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
<<<<<<< HEAD

            # Mostrar el pronóstico con la información del clima y fenómenos
            print(f"{fecha}: {clima} con una temperatura de {temperatura}{símbolo_medida[unidad_de_medida]}.")
            print(f"Temperatura máxima: {temp_max:.2f}{símbolo_medida[unidad_de_medida]}, mínima: {temp_min:.2f}{símbolo_medida[unidad_de_medida]}.")
            print(f"Humedad: {humedad}%") 
            print(f"Velocidad del viento: {wind_vel} m/s, Dirección: {wind_dir}°.\n")

            if alerta:
                print(alerta)  # Mostrar alerta si hay un fenómeno peligroso
            print()  # Espacio en blanco entre los días
            informacion = {
                "temp_actual": temperatura,
                "temp_max": temp_max,
                "temp_min": temp_min,
                "humedad": humedad,
                "clima": clima,
                "viento_vel": wind_vel,
                "viento_dir": wind_dir
            }

            # Verificar si hay alertas meteorológicas en los datos recibidos
=======
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
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6
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
<<<<<<< HEAD
            lineas = archivo.readlines()
            if len(lineas) == 0:
                print("No hay consultas en el historial.")
                return
            
            print("1. Ver últimas 5 consultas")
            print("2. Buscar consulta por ciudad")
            print("3. Borrar historial")  
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                ultimas_consultas = obtener_ultimas_consultas()
                if not ultimas_consultas:
                    print("No hay consultas recientes.")
                    return

                # Mostrar las consultas completas
                for i, consulta in enumerate(ultimas_consultas, 1):
                    print(f"{i}.")
                    for linea in consulta:
                        print(linea, end="")
                    print()

                seleccion = input("Seleccione una ciudad (número): ")
                try:
                    seleccion = int(seleccion) - 1
                    if 0 <= seleccion < len(ultimas_consultas):
                        ciudad, pais = ultimas_consultas[seleccion][1].split(": ")[1].strip().split(", ")
                        obtener_clima(ciudad, pais)
                    else:
                        print("Selección no válida.")
                except ValueError:
                    print("Por favor, ingrese un número entero válido.")
            elif opcion == "2":
                ciudad = input("Ingrese el nombre de la ciudad a buscar: ").lower()
                print(f"\nConsultas relacionadas con {ciudad}:\n")
                encontrado = False
                for linea in lineas:
                    if ciudad in linea.lower():
                        print(linea, end="")
                        encontrado = True
                if not encontrado:
                    print(f"No se encontraron consultas para la ciudad: {ciudad}")
            elif opcion == "3":
                borrar_historial()
            else:
                print("Opción no válida.")
    
=======
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
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6
    except FileNotFoundError:
        flash("El archivo de historial no existe aún. No se han registrado consultas.")
    
    for consulta in consultas:
        if 'ciudad' not in consulta or 'pais' not in consulta:
            flash("Una de las entradas no tiene los datos necesarios para realizar una nueva consulta.")
            continue
    return render_template('ver_historial.html', consultas=consultas)

<<<<<<< HEAD

# Función para borrar el contenido del historial
=======
@app.route('/borrar_historial', methods=['POST'])
>>>>>>> f873fd3292e0a07bb858c536fa891417352f51a6
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