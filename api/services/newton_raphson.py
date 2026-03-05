"""
Motor matemático para el método de Newton-Raphson.
Utiliza SymPy para el procesamiento simbólico de funciones matemáticas.
"""

from sympy import Symbol, sympify, SympifyError
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

x = Symbol("x") # definimos x 

# Transformaciones para el parser que permiten sintaxis más flexible
# - standard_transformations: conversiones básicas
# - implicit_multiplication_application: permite "2x" en lugar de "2*x"
# - convert_xor: convierte ^ a ** (exponenciación)
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def parsear_funcion(funcion_texto: str):
    """
    Convierte una función matemática en texto a una expresión simbólica de SymPy.

    Esta función toma una cadena de texto que representa una función matemática
    y la convierte en una expresión simbólica que Python puede evaluar y manipular.

    Args:
        funcion_texto: String con la función matemática (ej: "x**2 - 4", "sin(x) - x/2")

    Returns:
        Expresión simbólica de SymPy que representa la función

    Raises:
        ValueError: Si la función no puede ser parseada o contiene sintaxis inválida

    Ejemplos:
        >>> parsear_funcion("x**2 - 4")
        x**2 - 4
        >>> parsear_funcion("sin(x) - x/2")
        sin(x) - x/2
        >>> parsear_funcion("2x + 1")  # multiplicación implícita
        2*x + 1
        >>> parsear_funcion("x^2")  # ^ como exponenciación
        x**2
    """
    if not funcion_texto or not funcion_texto.strip():
        raise ValueError("La función no puede estar vacía")

    funcion_texto = funcion_texto.strip()

    try:
        # Parseamos la expresión con las transformaciones definidas
        expresion = parse_expr(
            funcion_texto,
            local_dict={"x": x},
            transformations=TRANSFORMATIONS,
        )

        # Verificamos que la expresión contenga la variable x o sea una constante válida
        # (una función constante como "5" es válida aunque no tenga x)
        simbolos_libres = expresion.free_symbols
        if simbolos_libres and simbolos_libres != {x}:
            simbolos_extra = simbolos_libres - {x}
            raise ValueError(
                f"La función contiene variables no permitidas: {simbolos_extra}. "
                "Solo se permite la variable 'x'."
            )

        return expresion

    except SympifyError as e:
        raise ValueError(
            f"No se pudo interpretar la función '{funcion_texto}'. "
            f"Verifica la sintaxis. Error: {str(e)}"
        )
    except Exception as e:
        raise ValueError(f"Error al procesar la función '{funcion_texto}': {str(e)}")
