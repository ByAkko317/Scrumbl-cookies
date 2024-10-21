from dotenv import load_dotenv
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
import os 
import requests
import time

class ApiRequestHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def make_request(self):
        try:
            # Realizar la solicitud con un timeout de 5 segundos
            response = requests.get(self.api_url, timeout=5)

            # Manejo de los códigos de estado HTTP
            if 200 <= response.status_code < 300:
                return {"status": "success", "data": response.json()}  # Procesar la respuesta JSON
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
    #funcion para reintentar la la solicitud, con 3 reintentos
    def retry_request(self, retries=3):
        for attempt in range(retries):
            result = self.make_request()
            if result["status"] == "success":
                return result
        return {"status": "error", "message": "Se agotaron los intentos. Intente más tarde."}
def mostrar_menu():
    print("Menú de opciones:\n")
    print("1. Consulta de clima según ciudad")
    print("2. Consulta de pronóstico según ciudad")
    print("3. Ver historial")
    print("4. Cambiar unidades")
    print("5. Salir\n")

def validar_ciudad():
    while True:
        ciudad = input("Por favor, introduce el nombre de una ciudad: ")
        
        if not ciudad.strip():#.strip es para asegurarse que el valor ingresado no esté vacío
            print("El nombre de la ciudad no puede estar vacío. Inténtalo de nuevo.")
            continue
        
        if not ciudad.replace(" ", "").isalpha():#.isalpha para corroborar que no hayan ni números ni caracteres especiales
            print("El nombre de la ciudad solo debe contener letras y espacios. Inténtalo de nuevo.")
            continue
        
        return ciudad

def validar_pais():
    while True:
        pais = input("Introduce el nombre del país de la ciudad: ")
        
        if not pais.strip():
            print("El nombre del país no puede estar vacío. Inténtalo de nuevo.")
            continue
        
        if not pais.replace(" ", "").isalpha():
            print("El nombre del país solo debe contener letras y espacios. Inténtalo de nuevo.")
            continue
        
        return pais

def obtener_clima(nombre_ciudad, nombre_pais):
    load_dotenv()#obtención de datos de .env
    api = os.getenv('API')
    unidad_de_medida = "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={nombre_ciudad},{nombre_pais}&lang=sp&appid={api}&units={unidad_de_medida}"
    
    api_handler = ApiRequestHandler(url)#construcción de objeto para el api request
    result = api_handler.retry_request()

    if result["status"] == "success":
        data = result["data"]#navegación dentro del JSON obtenido en formato diccionario, utilizando slicing
        clima = data['weather'][0]['description']
        temperatura = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        print(f"El clima en {nombre_ciudad}, {nombre_pais} es: {clima} con una temperatura de {temperatura}°C.")
        print(f"Temperatura máxima: {temp_max}°C, Temperatura mínima: {temp_min}°C.")
    else:
        print(result["message"])

def obtener_pronostico(nombre_ciudad, nombre_pais):
    load_dotenv()
    api = os.getenv('API')
    unidad_de_medida = "metric"
    url_pronostico = f"https://api.openweathermap.org/data/2.5/forecast?q={nombre_ciudad},{nombre_pais}&cnt=40&lang=sp&appid={api}&units={unidad_de_medida}"
    
    api_handler = ApiRequestHandler(url_pronostico)
    result = api_handler.retry_request()
    pronosticos_por_dia = {}
    if result["status"] == "success":
        data = result["data"]
        print(f"Pronóstico de 5 días para {nombre_ciudad}, {nombre_pais}:\n")
        # Filtrar registros de las 12:00 de cada día y calcular la media de temp. máxima y mínima
        for item in data['list']:
            fecha = item['dt_txt'].split(" ")[0]  # Obtener solo la fecha
            hora = item['dt_txt'].split(" ")[1]   # Obtener la hora

            # Elegir el pronóstico de las 12:00 de cada día
            if hora == "12:00:00":
                pronosticos_por_dia[fecha] = {
                    "clima": item['weather'][0]['description'],
                    "temp": item['main']['temp'],
                    "temp_max": item['main']['temp_max'],
                    "temp_min": item['main']['temp_min'],
                    "fenomenos": item['weather'][0]['main']  # Fenómenos meteorológicos
                }

        # Mostrar el pronóstico para los próximos 5 días con fenómenos meteorológicos
        for fecha, item in pronosticos_por_dia.items():
            clima = item['clima']
            temp = item['temp']
            temp_max = item['temp_max']
            temp_min = item['temp_min']
            fenomenos = item['fenomenos']

            # Identificar posibles fenómenos meteorológicos peligrosos
            alerta = ""
            if fenomenos in ['Rain', 'Thunderstorm', 'Snow']:
                alerta = f"¡Atención! Se esperan {fenomenos.lower()}."

            # Mostrar el pronóstico con la información del clima y fenómenos
            print(f"{fecha}: {clima} con una temperatura de {temp}°C.")
            print(f"Temperatura máxima: {temp_max:.2f}°C, mínima: {temp_min:.2f}°C.")
            if alerta:
                print(alerta)  # Mostrar alerta si hay un fenómeno peligroso
            print()  # Espacio en blanco entre los días
    else:
        print(result["message"])

def ver_historial():
    print("Ver historial")

def cambiar_unidades():
    print("Cambiar Unidades")

def ejecutar_opcion(opcion):
    if opcion == 1:
        nombre_ciudad = validar_ciudad()
        nombre_pais = validar_pais()
        obtener_clima(nombre_ciudad, nombre_pais)
    elif opcion == 2:
        nombre_ciudad = validar_ciudad()
        nombre_pais = validar_pais()
        obtener_pronostico(nombre_ciudad, nombre_pais)
    elif opcion == 3:
        ver_historial()
    elif opcion == 4:
        cambiar_unidades()
    elif opcion == 5:
        print("Saliendo del programa...")
        return False
    else:
        print("Opción no válida.")
    return True

def preguntar_volver_al_menu():
    while True:
        respuesta = input("¿Desea volver al menú? (si/no): ").strip().lower()
        if respuesta == 'si':
            return True  # Volver al menú
        elif respuesta == 'no':
            print("Saliendo del programa...")
            return False  # Finalizar programa
        else:
            print("Respuesta no válida. Por favor, ingresa 'si' para sí o 'no' para no.")

def main():
    while True:#funcion main del codigo, donde se hace las llamadas originales
        mostrar_menu()#llamada a la función menú
        try:
            seleccion = int(input("Selecciona una opción (1-5): "))
            continuar = ejecutar_opcion(seleccion)
            if not continuar:
                break
            if not preguntar_volver_al_menu():#llamada la función que al finalizar la ejecución de alguna de las opciones del menú, consulte si volver al mismo o salir
                break
            time.sleep(2)
        except ValueError:
            print("Por favor, ingresa un número entero válido.")
            time.sleep(2)

if __name__ == "__main__":
    main()
