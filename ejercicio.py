try:
    # Código que puede generar una excepción
    result = 10 / 0  # Esto genera una excepción ZeroDivisionError
except ZeroDivisionError as e:  # Captura la excepción y la asigna a la variable 'e'
    print(f"Ocurrió un error: {e}")  # 'e' contiene el mensaje de la excepción
