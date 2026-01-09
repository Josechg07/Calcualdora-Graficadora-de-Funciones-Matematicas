import numpy as np
import matplotlib.pyplot as plt



def generar_x(x_min=-10, x_max=10, puntos=1000):

    return np.linspace(x_min, x_max, puntos)



def graficar(x, lista_funciones):

    plt.figure()
    
    colores = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow', 'black']
    
    for i, (y, expresion) in enumerate(lista_funciones):
        color_actual = colores[i % len(colores)]
        plt.plot(x, y, label=f"f(x)={expresion}", color=color_actual)

    #Ejes
    plt.axhline(0, linewidth=0.8, color='black')
    plt.axvline(0, linewidth=0.8, color='black')
    #Cuadrícula
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gráfico de Funciones")
    plt.legend()
    plt.tight_layout()
    plt.show()
    