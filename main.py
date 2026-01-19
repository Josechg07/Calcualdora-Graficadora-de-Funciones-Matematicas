import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graficador import obtener_figura, generar_x
from parser_funciones import evaluar_con_lark

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Axis 2D")
        self.root.geometry("1000x800")

        # Variables
        self.lista_funciones = []
        self.x_min_var = tk.StringVar(value="-10")
        self.x_max_var = tk.StringVar(value="10")
        self.funcion_var = tk.StringVar()

        # Layout pricipal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel de Control (Izquierda)
        control_panel = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Entradas de Rango
        ttk.Label(control_panel, text="Rango X Min:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(control_panel, textvariable=self.x_min_var).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(control_panel, text="Rango X Max:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(control_panel, textvariable=self.x_max_var).pack(fill=tk.X, pady=(0, 10))

        # Entrada de Función
        ttk.Label(control_panel, text="Nueva Función f(x):").pack(anchor=tk.W, pady=(10, 5))
        entry_func = ttk.Entry(control_panel, textvariable=self.funcion_var)
        entry_func.pack(fill=tk.X, pady=(0, 5))
        entry_func.bind('<Return>', lambda e: self.agregar_funcion())

        ttk.Button(control_panel, text="Agregar Función", command=self.agregar_funcion).pack(fill=tk.X, pady=(0, 10))

        # Lista de Funciones
        ttk.Label(control_panel, text="Funciones Activas:").pack(anchor=tk.W, pady=(10, 5))
        self.listbox_funciones = tk.Listbox(control_panel, height=10)
        self.listbox_funciones.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        ttk.Button(control_panel, text="Eliminar Función Seleccionada", command=self.eliminar_funcion).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(control_panel, text="Limpiar Todas Las Funciones", command=self.limpiar_todo).pack(fill=tk.X, pady=(0, 5))

        # Panel de Gráfico (Derecha)
        self.graph_panel = ttk.Frame(main_frame)
        self.graph_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Inicializar gráfico vacío
        self.canvas = None
        self.actualizar_grafico()

    def agregar_funcion(self):
        expresion = self.funcion_var.get().strip()
        if not expresion:
            return

        # Validamos primero
        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
            if x_min >= x_max:
                messagebox.showerror("Error", "X Min debe ser menor que X Max")
                return
            
            # Prueba rápida de parsing
            # Usamos un rango pequeño para validar
            x_test = generar_x(x_min, x_max, puntos=10)
            evaluar_con_lark(expresion, x_test)
            
            self.lista_funciones.append(expresion)
            self.listbox_funciones.insert(tk.END, expresion)
            self.funcion_var.set("") # Limpiar entrada
            self.actualizar_grafico()

        except Exception as e:
            messagebox.showerror("Error de Sintaxis", f"No se pudo interpretar la función:\n{e}")

    def eliminar_funcion(self):
        seleccion = self.listbox_funciones.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista_funciones.pop(index)
            self.listbox_funciones.delete(index)
            self.actualizar_grafico()

    def limpiar_todo(self):
        self.lista_funciones = []
        self.listbox_funciones.delete(0, tk.END)
        self.actualizar_grafico()

    def actualizar_grafico(self):
        # Limpiar canvas anterior si existe
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            plt.close('all') # Cerrar figuras de matplotlib para liberar memoria

        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
        except ValueError:
            return # Esperar a que sean números válidos

        if x_min >= x_max:
             return

        x = generar_x(x_min, x_max, puntos=1000)
        
        # Preparar datos para obtener_figura
        # obtener_figura espera lista de tuplas (y, expresion)
        datos_para_graficar = []
        for expresion in self.lista_funciones:
            try:
                y = evaluar_con_lark(expresion, x)
                datos_para_graficar.append((y, expresion))
            except Exception as e:
                print(f"Error al graficar {expresion}: {e}")
        
        fig = obtener_figura(x, datos_para_graficar)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()