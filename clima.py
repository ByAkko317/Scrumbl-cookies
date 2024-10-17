from dotenv import load_dotenv
import os 
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

nombre_ciudad=input("Ingrese la ciudad para obtener su pronóstico: ")
nombre_pais=input("Ingrese el pais de la ciudad: ")

load_dotenv()
api= os.getenv('API')
unidad_de_medida="metric"#tiene distintas variantes, por default es kelvin, y el resto son metric(celsius) e imperial(fahrenheit),
url= f"https://api.openweathermap.org/data/2.5/weather?q={nombre_ciudad},{nombre_pais}&appid={api}&units={unidad_de_medida}"
lat=0
long=0
respuesta_api=requests.get(url)
#validacion de la respuesta de la api
if respuesta_api.status_code == 200:
    clima=respuesta_api.json()#guardo el archivo en formato json q me permite navegar como si fuese un diccionario por la data
    print(clima)#obtengo los datos de la llave
    lat=clima['coord']['lat']
    long=clima['coord']['lon']
    print(type(lat)) #obtengo los datos de lat y lon para utilizar el resto de url de api que no usan geocoding (nombre de ciudad como parametro)
else: 
    print(f"Error: {respuesta_api.status_code}")

#segmento tira error, no funciona aún
# url_pronostico=f"api.openweathermap.org/data/2.5/forecast?q={nombre_ciudad},{nombre_pais}&appid={api}&units={unidad_de_medida}"
# respuesta_api2=requests.get(url_pronostico)
# if respuesta_api.status_code == 200:
#     pronostico=respuesta_api.json()
#     print(pronostico)
# else: 
#     print(f"Error: {respuesta_api.status_code}")

#apartado de manejo de errores en base a una clase con sus funciones correspondientes
class ApiRequestHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def make_request(self):
        try:
            # Realizar la solicitud con un timeout de 5 segundos
            response = requests.get(self.api_url, timeout=5)
            
            # Manejo de los códigos de estado HTTP
            if 200 <= response.status_code < 300:
                # Solicitud exitosa
                print("Solicitud exitosa.")
                return response.json()  # Procesar la respuesta JSON
            elif response.status_code == 400:
                print("Solicitud inválida, por favor revise los datos ingresados.")
            elif response.status_code == 401:
                print("Autenticación fallida, por favor verifique sus credenciales.")
            elif response.status_code == 404:
                print("Datos no encontrados, por favor verifique la información proporcionada.")
            elif response.status_code == 500:
                print("Error en el servidor, intente más tarde.")
            elif 502 <= response.status_code <= 504:
                print("API no disponible, intente más tarde.")
            else:
                print(f"Error inesperado: {response.status_code}")
                
        except Timeout:
            print("La solicitud ha tardado demasiado. Verifique su conexión e intente de nuevo.")
        except ConnectionError:
            print("Error de conexión. Verifique su conexión a Internet.")
        except HTTPError as http_err:
            print(f"Error HTTP: {http_err}")
        except RequestException as req_err:
            print(f"Error en la solicitud: {req_err}")
        except Exception as err:
            print(f"Ocurrió un error inesperado: {err}")     
        return None

    def retry_request(self, retries=3):
        # Intentar la solicitud varias veces en caso de fallo temporal
        for attempt in range(retries):
            print(f"Intento {attempt + 1} de {retries}")
            result = self.make_request()
            if result is not None:
                return result
        print("Se agotaron los intentos. Intente más tarde.")
        return None
