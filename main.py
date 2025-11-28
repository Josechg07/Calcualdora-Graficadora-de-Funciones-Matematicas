from graficador import generar_x, graficar
from parser_funciones import evaluar_con_lark


def main():
    print("=== Calculadora Graficadora 2D ===")
    print("Escribe una función en x.")
    print("Puedes usar: +, -, *, /, ^, (), ")
    print("x, sin, cos, tan, log, exp, sqrt, pi, e")
    print()

    expresion = input("f(x) = ")

    try:
        x_min = float(input("x mínimo (ej. -10): "))
        x_max = float(input("x máximo (ej. 10): "))

    except ValueError:
        print("Rango inválido. Usar -10 a 10.")
        x_min, x_max = -10.0, 10.0


    if x_min >= x_max:
        print("x_min debe ser menor que x_max. Usar -10 a 10")
        x_min, x_max = -10, 10


    x = generar_x(x_min, x_max, puntos=1000) # preguntar a Jose 



    try:
        y = evaluar_con_lark(expresion, x)

    except Exception as e:
        print("\Ocurrió un error al interpretar la expresión:")
        print(e)
        return
    

    graficar(x, y, expresion)



if __name__ == "__main__":
    main()