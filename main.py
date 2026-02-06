import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graficador import obtener_figura, generar_x
from parser_funciones import evaluar_con_lark
import numpy as np

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Axis 2D")
        self.root.geometry("1000x800")

        # Variables
        self.lista_funciones = []
        self.x_min_var = tk.StringVar(value="-10")
        self.x_max_var = tk.StringVar(value="10")
        self.y_min_var = tk.StringVar(value="-10")
        self.y_max_var = tk.StringVar(value="10")
        self.funcion_var = tk.StringVar()
        self.funcion_x_var = tk.StringVar()
        self.funcion_y_var = tk.StringVar()
        self.mode = "normal" # "normal" or "parametric"

        # Layout pricipal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel de Control (Izquierda)
        control_panel = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Mode Selection
        mode_frame = ttk.Frame(control_panel)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(mode_frame, text="Normal Mode (y=f(x))", command=self.set_normal_mode).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(mode_frame, text="Parametric Mode (x(t), y(t))", command=self.set_parametric_mode).pack(fill=tk.X)

        # Entradas de Rango X
        ttk.Label(control_panel, text="Rango X Min:").pack(anchor=tk.W, pady=(0, 5))
        entry_xmin = ttk.Entry(control_panel, textvariable=self.x_min_var)
        entry_xmin.pack(fill=tk.X, pady=(0, 10))
        entry_xmin.bind('<Return>', lambda e: self.actualizar_grafico())

        ttk.Label(control_panel, text="Rango X Max:").pack(anchor=tk.W, pady=(0, 5))
        entry_xmax = ttk.Entry(control_panel, textvariable=self.x_max_var)
        entry_xmax.pack(fill=tk.X, pady=(0, 10))
        entry_xmax.bind('<Return>', lambda e: self.actualizar_grafico())

        # Entradas de Rango Y
        ttk.Label(control_panel, text="Rango Y Min:").pack(anchor=tk.W, pady=(0, 5))
        entry_ymin = ttk.Entry(control_panel, textvariable=self.y_min_var)
        entry_ymin.pack(fill=tk.X, pady=(0, 10))
        entry_ymin.bind('<Return>', lambda e: self.actualizar_grafico())

        ttk.Label(control_panel, text="Rango Y Max:").pack(anchor=tk.W, pady=(0, 5))
        entry_ymax = ttk.Entry(control_panel, textvariable=self.y_max_var)
        entry_ymax.pack(fill=tk.X, pady=(0, 10))
        entry_ymax.bind('<Return>', lambda e: self.actualizar_grafico())

        ttk.Button(control_panel, text="Actualizar Rango", command=self.actualizar_grafico).pack(fill=tk.X, pady=(0, 10))

        # Functio Input Area
        self.input_frame_normal = ttk.Frame(control_panel)
        self.input_frame_normal.pack(fill=tk.X)
        
        self.input_frame_parametric = ttk.Frame(control_panel)
        # Hidden by default
        
        # Normal Input
        ttk.Label(self.input_frame_normal, text="Nueva Función f(x):").pack(anchor=tk.W, pady=(10, 5))
        entry_func = ttk.Entry(self.input_frame_normal, textvariable=self.funcion_var)
        entry_func.pack(fill=tk.X, pady=(0, 5))
        entry_func.bind('<Return>', lambda e: self.agregar_funcion())
        
        # Parametric Input
        ttk.Label(self.input_frame_parametric, text="Función x(t):").pack(anchor=tk.W, pady=(10, 5))
        entry_func_x = ttk.Entry(self.input_frame_parametric, textvariable=self.funcion_x_var)
        entry_func_x.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(self.input_frame_parametric, text="Función y(t):").pack(anchor=tk.W, pady=(5, 5))
        entry_func_y = ttk.Entry(self.input_frame_parametric, textvariable=self.funcion_y_var)
        entry_func_y.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(control_panel, text="Agregar Función", command=self.agregar_funcion).pack(fill=tk.X, pady=(10, 10))

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

    def set_normal_mode(self):
        self.mode = "normal"
        self.actualizar_visibilidad_inputs()

    def set_parametric_mode(self):
        self.mode = "parametric"
        self.actualizar_visibilidad_inputs()

    def actualizar_visibilidad_inputs(self):
        if self.mode == "normal":
            self.input_frame_parametric.pack_forget()
            # To maintain order, we might need to repack things or use a container
            # For simplicity in this edit, let's just use pack/pack_forget and hope for the best, 
            # or I can fix the order in the next step.
            self.input_frame_normal.pack(fill=tk.X)
        else:
            self.input_frame_normal.pack_forget()
            self.input_frame_parametric.pack(fill=tk.X)

    def agregar_funcion(self):
        if self.mode == "normal":
            expresion = self.funcion_var.get().strip()
            if not expresion: return
            label = f"f(x)={expresion}"
            data = {"mode": "normal", "expr": expresion}
        else:
            expr_x = self.funcion_x_var.get().strip()
            expr_y = self.funcion_y_var.get().strip()
            if not expr_x or not expr_y: return
            label = f"x={expr_x}\ny={expr_y}"
            data = {"mode": "parametric", "expr_x": expr_x, "expr_y": expr_y}

        # Validamos primero
        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
            if x_min >= x_max:
                messagebox.showerror("Error", "X Min debe ser menor que X Max")
                return
            
            # Prueba rápida de parsing
            if self.mode == "normal":
                x_test = generar_x(x_min, x_max, puntos=10)
                evaluar_con_lark(data["expr"], x_test)
            else:
                t_test = np.linspace(0, 1, 10)
                # Pass dummy x because it's required by EvaluadorLark.__init__
                dummy_x = np.zeros(10)
                evaluar_con_lark(data["expr_x"], dummy_x, t_test)
                evaluar_con_lark(data["expr_y"], dummy_x, t_test)
            
            self.lista_funciones.append(data)
            self.listbox_funciones.insert(tk.END, label)
            
            # Limpiar entradas
            self.funcion_var.set("")
            self.funcion_x_var.set("")
            self.funcion_y_var.set("")
            
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
            y_min = float(self.y_min_var.get())
            y_max = float(self.y_max_var.get())
        except ValueError:
            return # Esperar a que sean números válidos

        if x_min >= x_max:
             return
        
        if y_min >= y_max:
            return

        x = generar_x(x_min, x_max, puntos=2000)
        t = np.linspace(0, 12 * np.pi, 2000)
        
        # Preparar datos para obtener_figura
        datos_para_graficar = []
        for data in self.lista_funciones:
            try:
                # Si es una cadena antigua (de sesiones previas o legacy), tratar como normal
                if isinstance(data, str):
                    expresion = data
                    y = evaluar_con_lark(expresion, x)
                    datos_para_graficar.append((y, expresion))
                    continue

                if data["mode"] == "normal":
                    expresion = data["expr"]
                    y = evaluar_con_lark(expresion, x)
                    datos_para_graficar.append((y, expresion))
                elif data["mode"] == "parametric":
                    expr_x = data["expr_x"]
                    expr_y = data["expr_y"]
                    # Evaluar x e y usando el parámetro t
                    x_vals = evaluar_con_lark(expr_x, x, t)
                    y_vals = evaluar_con_lark(expr_y, x, t)
                    # Añadir como una única curva paramétrica (x_vals vs y_vals)
                    datos_para_graficar.append((x_vals, y_vals, f"x={expr_x}\ny={expr_y}"))
            except Exception as e:
                print(f"Error al graficar {data}: {e}")
        
        # Generar la figura con los datos recolectados
        fig = obtener_figura(x, datos_para_graficar, y_min, y_max)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()

    