'''from dotenv import load_dotenv
import os''' 
import requests

nombre_ciudad=input("Ingrese la ciudad para obtener su pronóstico: ")
nombre_pais=input("Ingrese el pais de la ciudad: ")

'''load_dotenv('/Proyecto Integrador/api.env')
api= os.getenv('api')
print(api)'''
api="abf47be9918bb6eb6fb7cdd893089636"
unidad_de_medida="metric"#tiene distintas variantes, por default es kelvin, y el resto son metric(celsius) e imperial(fahrenheit),
url= f"https://api.openweathermap.org/data/2.5/weather?q={nombre_ciudad},{nombre_pais}&appid={api}&units={unidad_de_medida}"
#Holis
respuesta_api=requests.get(url)
#validacion de la respuesta de la api
if respuesta_api.status_code == 200:
    clima=respuesta_api.json()#guardo el archivo en formato json q me permite navegar como si fuese un diccionario por la data
    print(clima['main'])#obtengo los datos de la llave
else: 
    print(f"Error: {respuesta_api.status_code}")
