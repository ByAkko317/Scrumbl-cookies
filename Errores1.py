
"""1 - Importa la bibloteca requests que realiza el manejo de las solictudes HTTP
Exceptions:
Timeout: Solicitud tarda demasiado
ConecctionError: Problema de conexión.
HTTPError: Error inesperado HTTP.
RequestException: Captura cualquier otro error relacionado con las solicitudes
2- Se define la clase ApiRequestHander (url de la API, y la almacena)
3- Método make_request que realiza la solicitud (envia solicitud GET, tiemout: 5)
4- Manejo de códigos de estado HTTP (éxito, solicitud inválida, no autorizado, no encontrado,
error del servidor, error de puerta enlace)
5- Excepciones capturan los errores durante la solcitud.
6- Método retry-request: se usa para reintentar las solicutudes
"""



import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

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

