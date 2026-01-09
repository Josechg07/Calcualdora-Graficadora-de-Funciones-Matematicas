from graficador import (generar_x, graficar)
from parser_funciones import evaluar_con_lark


def main():
    print("=== Calculadora Graficadora 2D -- Múltiples Funciones ===")
    print("Escribe una función en x.")
    print("Puedes usar: +, -, *, /, ^, (), ")
    print("x, sin, cos, tan, log, exp, sqrt, pi, e")
    print()

    # 1. Pedir rango primero
    try:
        x_min = float(input("x mínimo (ej. -10): "))
        x_max = float(input("x máximo (ej. 10): "))
    except ValueError:
        print("Rango inválido. Usar -10 a 10.")
        x_min, x_max = -10.0, 10.0

    if x_min >= x_max:
        print("x_min debe ser menor que x_max. Usar -10 a 10")
        x_min, x_max = -10, 10

    x = generar_x(x_min, x_max, puntos=1000)
    
    lista_funciones = []

    while True:
        expresion = input("\nIngresa una función f(x) = ")

        try:
            # Evaluamos para ver si es válida
            y = evaluar_con_lark(expresion, x)
            # Guardamos la tupla (valores_y, texto_expresion)
            lista_funciones.append((y, expresion))
            print(f"Función '{expresion}' agregada correctamente.")

        except Exception as e:
            print("Ocurrió un error al interpretar la expresión:")
            print(e)
            print("Intenta nuevamente.")
        
        # Preguntar si quiere otra
        continuar = input("¿Deseas agregar otra función? (s/n): ").strip().lower()
        if continuar != 's':
            break
    
    if not lista_funciones:
        print("No se agregaron funciones para graficar.")
        return

    graficar(x, lista_funciones)



if __name__ == "__main__":
    main()