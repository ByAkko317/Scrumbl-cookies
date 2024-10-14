# Desarrollar la funcionalidad que permite al usuario introducir el nombre de una ciudad. 

ciudad = input("Por favor, introduce el nombre de una ciudad: ")

def validar_ciudad():
    while True:
        ciudad = input("Por favor, introduce el nombre de una ciudad: ")
        
        if not ciudad.strip():
            print("El nombre de la ciudad no puede estar vacío. Inténtalo de nuevo.")
            continue
        
        if not ciudad.replace(" ", "").isalpha():
            print("El nombre de la ciudad solo debe contener letras y espacios. Inténtalo de nuevo.")
            continue
        
        return ciudad

ciudad = validar_ciudad()



