def obtener_clima(nombre_ciudad, nombre_pais):
    load_dotenv()  # obtención de datos de .env
    api = os.getenv('API')
    global unidad_de_medida
    url = f"https://api.openweathermap.org/data/2.5/weather?q={nombre_ciudad},{nombre_pais}&lang=sp&appid={api}&units={unidad_de_medida}"

    símbolo_medida = { 
        "metric": "ºC",
        "imperial": "ºF"
    }

    api_handler = ApiRequestHandler(url)  # construcción de objeto para el api request
    result = api_handler.retry_request()

    if result["status"] == "success":
        data = result["data"]  # navegación dentro del JSON obtenido en formato diccionario

        clima = data['weather'][0]['description']
        temperatura = data['main']['temp']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        humedad = data['main']['humidity']  # Obtener la humedad

        print(f"El clima en {nombre_ciudad}, {nombre_pais} es: {clima} con una temperatura de {temperatura} {símbolo_medida[unidad_de_medida]}.")
        print(f"Temperatura máxima: {temp_max}{símbolo_medida[unidad_de_medida]}, Temperatura mínima: {temp_min}{símbolo_medida[unidad_de_medida]}.")
        print(f"Humedad: {humedad}%")  # Mostrar el porcentaje de humedad

        # Preparar información para guardar en el historial
        informacion = {
            "temp_actual": temperatura,
            "temp_max": temp_max,
            "temp_min": temp_min,
            "humedad": humedad,  # Agregar la humedad a la información
            "clima": clima
        }

        # Verificar si hay alertas meteorológicas en los datos recibidos
        if 'alerts' in data:
            informacion['alerta'] = data['alerts'][0]['description']

        # Llamar a la función para guardar en el historial
        guardar_en_historial(nombre_ciudad, nombre_pais, informacion)
    else:
        print(result["message"])
