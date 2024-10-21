



unidad_de_medida = "metric"  # Valor por defecto

def cambiar_unidades():
    global unidad_de_medida  # Usar la variable global
    print(f"Unidad de medida actual: {'Celsius' if unidad_de_medida == 'metric' else 'Fahrenheit'}")
    print("Selecciona la unidad de medida:")
    print("1. Métrico (Celsius)")
    print("2. Imperial (Fahrenheit)")

    while True:
        seleccion = input("Ingresa tu opción: ")
        if seleccion == '1':
            if unidad_de_medida == 'metric':
                print("Ya estás utilizando la unidad de medida: Celsius.")
            else:
                unidad_de_medida = 'metric'  # Cambiar a Celsius
                print("Unidad de medida cambiada a Celsius.")
                break  # Salir del bucle
        elif seleccion == '2':
            if unidad_de_medida == 'imperial':
                print("Ya estás utilizando la unidad de medida: Fahrenheit.")
            else:
                unidad_de_medida = 'imperial'  # Cambiar a Fahrenheit
                print("Unidad de medida cambiada a Fahrenheit.")
                break  # Salir del bucle
        else:
            print("Opción no válida. Intenta de nuevo.")

# Ejemplo de uso
cambiar_unidades()