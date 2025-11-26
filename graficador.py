import numpy as np
import matplotlib.pyplot as plt



def generar_x(x_min=-10, x_max=10, puntos=1000):

    return np.linspace(x_min, x_max, puntos)


def graficar(x, y, expresion):

    plt.figure()
    plt.plot(x, y)
    #Ejes
    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)
    #Cuadrícula
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"f(x) = {expresion}")
    plt.tight_layout()
    plt.show()
    