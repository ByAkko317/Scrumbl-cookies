import time
import os

while True:
    print ("\n MENÚ\n ")
    print ("¿Qué hacemos?\n \n 1) Elegir CIUDAD\n 2) Elegir Unidad de Medida\n 3) Ver Pronósticos Futuros\n 4) Salir\n ")

    switcher = {
        1: eleccionCiudad,
        2: eleccionUnidad,
        3: eleccionDia,
        4: finalizar,
    }
    opcion = input    
    if isinstance(opcion, int):
        print("¡Perfecto! Has ingresado una cadena.")
        break
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Eso no es una cadena. Intenta de nuevo.")

def eleccionCiudad():
    #algoritmo con buscador de API

    while True:
        ciudad= input("Por favor ingrese nombre de ciudad\n ")
        if isinstance(ciudad, str):
            print("¡Perfecto! Tipo de dato válido")
            time.sleep(2)
            print("Cargando...")
            time.sleep(3)

            urlApi = ""
            params = {
                'Ciudad': 'ciudad'
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
    # Parsear el contenido en JSON
                data = response.json()
    
    # Mostrar los datos (esto depende de la estructura de los datos)
                for item in data:
                    print("ID:", item["id"])
                    print("Ciudad:", item["ciudad"])
                    print("dato1:", item["dato1"])
                    print("dato2", item["dato2"])
                    print("---")
            else:
                print("Error:", response.status_code)
                break
        else:
            print("Dato incorrecto. Intenta de nuevo")

    

os.system('cls' if os.name == 'nt' else 'clear')


def eleccionUnidad():
    #algoritmo con cálculo y conexion y guardar dato
    return unidad

def eleccionDia():
    #dentro del rango de los siete días
    return dia