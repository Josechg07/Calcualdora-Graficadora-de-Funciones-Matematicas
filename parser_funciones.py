from lark import Lark, Transformer
import numpy as np

# Gramática de las expresiones matemáticas
GRAMATICA = r"""
?start: expr

?expr: expr "+" term   -> suma
     | expr "-" term   -> resta
     | term

?term: term factor -> mul
     | term "*" factor -> mul
     | term "/" factor -> div
     | term "x" factor -> mul
     | factor

?factor: factor "^" atom -> pot
       | atom

?atom: "-" atom            -> neg
    | NUMBER              -> numero
    | "X"                 -> variable
    | CONST               -> constante
    | NAME "(" expr ("," expr)? ")"   -> funcion
    | "(" expr ")"

CONST: "pi" | "e"

%import common.NUMBER
%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""

# Parser principal de Lark
parser = Lark(GRAMATICA, start="start", parser="lalr")


class EvaluadorLark(Transformer):
    """
    Recorre el árbol sintáctico generado por Lark y lo convierte
    en operaciones de NumPy para obtener y = f(x).
    """

    def __init__(self, x: np.ndarray):
        super().__init__()
        self.x = x

    # ----------- valores básicos -----------

    def numero(self, args):
        (valor,) = args
        return float(valor)

    def constante(self, args):
        (nombre,) = args
        nombre = str(nombre)
        if nombre == "pi":
            return np.pi
        elif nombre == "e":
            return np.e
        else:
            raise ValueError(f"Constante no soportada: {nombre}")

    def variable(self, _):
        # La variable x se reemplaza por el arreglo de NumPy
        return self.x

    # ----------- operaciones aritméticas -----------

    def suma(self, args):
        a, b = args
        return a + b

    def resta(self, args):
        a, b = args
        return a - b

    def mul(self, args):
        a, b = args
        return a * b

    def div(self, args):
        a, b = args
        return a / b

    def pot(self, args):
        a, b = args
        return a ** b

    def neg(self, args):
        (a,) = args
        return -a

    # ----------- funciones matemáticas -----------

    def funcion(self, args):
        nombre_token = args[0]
        nombre = str(nombre_token)

        # valor siempre es el primer argumento después del nombre
        if len(args) == 2:
            valor = args[1]
            base = None
        elif len(args) == 3:
            valor = args[1]
            base = args[2]
        else:
            raise ValueError(f"Número de argumentos inválido para la función {nombre}")

        funciones = {
            "sen": np.sin,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "sqrt": np.sqrt,
            "sec": lambda t: 1 / np.cos(t),
            "csc": lambda t: 1 / np.sin(t),
            "ctg": lambda t: 1 / np.tan(t),
            "sinh": np.sinh,
            "cosh": np.cosh,
            "tanh": np.tanh,
            "sech": lambda t: 1/ np.cosh(t),
            "csch": lambda t: 1/ np.sinh(t),
            "ctgh": lambda t: 1/ np.tanh(t),
            "abs": np.abs,
            "log10": np.log10,
            "ln": np.log,
        }

        if nombre == "log":
            # log(valor) -> ln(valor)
            # log(valor, base) -> log base 'base'
            if base is None:
                return np.log(valor)
            else:
                return np.log(valor) / np.log(base)

        if nombre not in funciones:
            raise ValueError(f"Función no soportada: {nombre}")

        if base is not None:
            raise ValueError(f"Función {nombre} no acepta un segundo argumento de base")

        return funciones[nombre](valor)


def evaluar_con_lark(expresion: str, x: np.ndarray) -> np.ndarray:
    """
    Evalúa una expresión matemática en función de x usando Lark.

    :param expresion: texto de la función, por ejemplo 'sin(x) + x^2'.
    :param x: arreglo de valores de x donde se quiere evaluar la función.
    :return: arreglo y = f(x) con el mismo tamaño que x.
    """
    tree = parser.parse(expresion)
    evaluador = EvaluadorLark(x)
    y = evaluador.transform(tree)
    return y
