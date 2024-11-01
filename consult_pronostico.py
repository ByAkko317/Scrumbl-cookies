import os
from dotenv import load_dotenv

def obtener_pronostico(nombre_ciudad, nombre_pais):
    load_dotenv()
    api = os.getenv('API')
    global unidad_de_medida
    url_pronostico = f"https://api.openweathermap.org/data/2.5/forecast?q={nombre_ciudad},{nombre_pais}&cnt=40&lang=sp&appid={api}&units={unidad_de_medida}"

    símbolo_medida = { 
        "metric": "ºC",
        "imperial": "ºF"
    }

    # Preguntar al usuario cómo desea ver el pronóstico
    print("Selecciona cómo quieres ver el pronóstico:")
    print("1. Muéstrame el pronóstico completo")
    print("2. Muéstrame un resumen")
    
    opcion = input("Elige una opción (1 o 2): ")

    api_handler = ApiRequestHandler(url_pronostico)
    result = api_handler.retry_request()
    pronosticos_por_dia = {}
    temperaturas = []
    climas = []
    fenomenos = []

    if result["status"] == "success":
        data = result["data"]
        
        # Filtrar registros de las 12:00 de cada día
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

                # Agregar datos a listas para análisis posterior
                temperaturas.append(item['main']['temp'])
                climas.append(item['weather'][0]['description'])
                fenomenos.append(item['weather'][0]['main'])

        if opcion == '1':
            # Mostrar el pronóstico completo
            print(f"\nPronóstico de 5 días para {nombre_ciudad}, {nombre_pais}:\n")
            for fecha, item in pronosticos_por_dia.items():
                clima = item['clima']
                temperatura = item['temp']
                temp_max = item['temp_max']
                temp_min = item['temp_min']
                fenomenos = item['fenomenos']

                # Identificar fenómenos peligrosos
                alerta = ""
                if fenomenos in ['Rain', 'Thunderstorm', 'Snow']:
                    alerta = f"¡Atención! Se esperan {fenomenos.lower()}."

                # Mostrar el pronóstico con la información del clima y fenómenos
                print(f"{fecha}: {clima} con una temperatura de {temperatura}{símbolo_medida[unidad_de_medida]}.")
                print(f"Temperatura máxima: {temp_max:.2f}{símbolo_medida[unidad_de_medida]}, mínima: {temp_min:.2f}{símbolo_medida[unidad_de_medida]}.")
                if alerta:
                    print(alerta)
                print()  # Espacio entre días

                informacion = {
                    "temp_actual": temperatura,
                    "temp_max": temp_max,
                    "temp_min": temp_min,
                    "clima": clima
                }

                # Guardar en el historial
                guardar_en_historial(nombre_ciudad, nombre_pais, informacion)

        elif opcion == '2':
            # Nueva funcionalidad: Resumen de pronósticos
            if temperaturas:
                temp_min = min(pronosticos_por_dia[fecha]['temp_min'] for fecha in pronosticos_por_dia)
                temp_max = max(pronosticos_por_dia[fecha]['temp_max'] for fecha in pronosticos_por_dia)
                promedio_temp = sum(temperaturas) / len(temperaturas)

                clima_mas_frecuente = max(set(climas), key=climas.count)
                fenomeno_mas_frecuente = max(set(fenomenos), key=fenomenos.count)

                print("\nResumen de pronósticos:")
                print(f"Temperatura mínima en 5 días: {temp_min:.2f}{símbolo_medida[unidad_de_medida]}")
                print(f"Temperatura máxima en 5 días: {temp_max:.2f}{símbolo_medida[unidad_de_medida]}")
                print(f"Temperatura promedio en 5 días: {promedio_temp:.2f}{símbolo_medida[unidad_de_medida]}")
                print(f"Clima más frecuente: {clima_mas_frecuente}")
                print(f"Fenómeno más frecuente: {fenomeno_mas_frecuente}")

        else:
            print("Opción no válida. Por favor, elige 1 o 2.")
    else:
        print(result["message"])
