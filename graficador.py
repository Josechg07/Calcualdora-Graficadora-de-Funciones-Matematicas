import numpy as np
import matplotlib.pyplot as plt



def generar_x(x_min=-10, x_max=10, puntos=1000):

    return np.linspace(x_min, x_max, puntos)



def obtener_figura(x, lista_funciones, y_min=-10, y_max=10):
    fig = plt.figure(facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_facecolor('black')
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y_min, y_max)
    
    colores = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow', 'white']
    
    for i, (y, expresion) in enumerate(lista_funciones):
        color_actual = colores[i % len(colores)]
        ax.plot(x, y, label=f"f(x)={expresion}", color=color_actual)

    #Ejes
    ax.axhline(0, linewidth=0.8, color='black')
    ax.axvline(0, linewidth=0.8, color='black')
    
    # Colores de los ejes y texto
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    #Cuadrícula
    ax.grid(True, linestyle="--", alpha=0.5, color='gray')
    
    ax.set_xlabel("x", color='white')
    ax.set_ylabel("y", color='white')
    ax.set_title("Gráfico de Funciones", color='white')
    
    legend = ax.legend(facecolor='black', edgecolor='white')
    plt.setp(legend.get_texts(), color='white')
    
    plt.tight_layout()
    return fig

def graficar(x, lista_funciones):
    fig = obtener_figura(x, lista_funciones)
    plt.show()
    