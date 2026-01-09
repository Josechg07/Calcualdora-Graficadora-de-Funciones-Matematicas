import re
from sympy import symbols, sympify, lambdify

class ProcesadorMatematico:
    def __init__(self):
        # Definimos 'x' como el símbolo principal de la calculadora
        self.x = symbols('x')

    def corregir_multiplicacion_implicita(self, expresion):
        """
        Transforma entradas como '2x' en '2*x' usando Expresiones Regulares.
        """
        # Insertar '*' entre un número y una letra: 2x -> 2*x
        expresion = re.sub(r'(\d)(?=[a-zA-Z])', r'\1*', expresion)
        # Insertar '*' entre letra y número: x2 -> x*2 (opcional)
        expresion = re.sub(r'([a-zA-Z])(?=\d)', r'\1*', expresion)
        # Insertar '' entre un número y un paréntesis: 2(x) -> 2(x)
        expresion = re.sub(r'(\d)(?=\()', r'\1*', expresion)
        # Insertar '*' entre un paréntesis y una letra/número: (x)2 -> (x)*2
        expresion = re.sub(r'\)(?=\w)', r')*', expresion)
        # Insertar '' entre dos paréntesis: (x)(x) -> (x)(x)
        expresion = re.sub(r'\)(?=\()', r')*', expresion)
        
        return expresion

    def obtener_funcion(self, entrada_usuario):
        """
        Convierte el texto del usuario en una función ejecutable de Python.
        """
        try:
            # 1. Limpiamos la entrada (el truco de la x)
            texto_corregido = self.corregir_multiplicacion_implicita(entrada_usuario)
            
            # 2. Convertimos a expresión de SymPy
            expresion_sympy = sympify(texto_corregido)
            
            # 3. Creamos una función de Python real (optimizada para cálculo)
            # Esto permite que evalúes la función pasando un número: f(5)
            f_evaluable = lambdify(self.x, expresion_sympy, 'numpy')
            
            return f_evaluable, texto_corregido
            
        except Exception as e:
            return None, str(e)

# --- EJEMPLO DE INTEGRACIÓN EN TU TERMINAL ---
if __name__ == "__main__":
    procesador = ProcesadorMatematico()
    
    print("--- Calculadora Gráfica (Pre-procesador activo) ---")
    entrada = input("Introduce la función (ej: 3x+1 o 2x(x+5)): ")
    
    funcion, detalle = procesador.obtener_funcion(entrada)
    
    if funcion:
        print(f"\n[Éxito] Interpretado como: {detalle}")
        # Ejemplo: Evaluar la función en x = 10
        valor_x = 10
        resultado = funcion(valor_x)
        print(f"Si x vale {valor_x}, el resultado es: {resultado}")
    else:
        print(f"\n[Error] No pude entender la función: {detalle}")