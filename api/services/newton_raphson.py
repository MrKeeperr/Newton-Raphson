from sympy import Symbol, lambdify, sympify, SympifyError, diff
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from api.models.schemas import NewtonRaphsonResponse, NewtonRaphsonResult

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

def calcular_derivada(funcion):
    """
    Calcula la derivada de una función simbólica con respecto a x.

    Args:
        funcion: Expresión simbólica de SymPy que representa la función

    Returns:
        Expresión simbólica de SymPy que representa la derivada de la función
    """
    return funcion.diff(x)

def ejecutar_newton_raphson(
        funcion_texto:str,
        x0:float,
        tolerancia:float=0.0001,
        max_iteraciones:int=50
) -> NewtonRaphsonResult:
    """
    Ejecuta el método de Newton-Raphson para encontrar una raíz de la función dada.

    Args:
        funcion_texto: String con la función matemática (ej: "x**2 - 4", "sin(x) - x/2")
        x0: Punto inicial para comenzar la iteración de Newton-Raphson
        tolerancia: Tolerancia para el error relativo para detener las iteraciones (default: 0.0001)
        max_iteraciones: Número máximo de iteraciones permitidas (default: 50)
    
    Returns:
        NewtonRaphsonResult con el resultado del cálculo
    """

    expresion = parsear_funcion(funcion_texto)
    derivada = diff(expresion, x)
    f = lambdify(x, expresion, modules=["math"]) # Crear funciones evaluadoras rápidas (lambdify convierte SymPy a NumPy)
    df = lambdify(x, derivada, modules=["math"])

    resultados: list[NewtonRaphsonResponse] = []
    iteracion = 0
    x_actual = x0
    error_actual = float("inf")  # Inicializamos con infinito

    while iteracion < max_iteraciones:
        valor_f = float(f(x_actual))
        valor_df = float(df(x_actual))
        
        if abs(valor_df) < 1e-9:
            resultados.append(
                NewtonRaphsonResponse(
                    paso=iteracion,
                    x_actual=x_actual,
                    f_x=valor_f,
                    f_derivada_x=valor_df,
                    error_relativo=error_actual
                    if error_actual != float("inf")
                    else None,
                )
            )
            return NewtonRaphsonResult(
                exito=False,
                mensaje=f"Error: Derivada cero (o muy cercana a cero) en x = {x_actual}. No se puede continuar.",
                iteraciones=resultados,
                raiz=None,
            )
        # fórmula de Newton-Raphson
        x_nuevo = x_actual - (valor_f / valor_df)
        # Calcular el error
        if abs(x_nuevo) < 1e-15:
            error_actual = abs(x_nuevo - x_actual)
        else:
            # Error relativo
            error_actual = abs((x_nuevo - x_actual) / x_nuevo)

        resultados.append(
            NewtonRaphsonResponse(
                paso=iteracion,
                x_actual=x_actual,
                f_x=valor_f,
                f_derivada_x=valor_df,
                error_relativo=error_actual,
            )
        )
        # Comprobar si ya hay convergencia
        if error_actual <= tolerancia:
            # Añadimos el valor final encontrado
            """resultados.append(
                NewtonRaphsonResponse(
                    paso=iteracion + 1,
                    x_actual=x_nuevo,
                    f_x=float(f(x_nuevo)),
                    f_derivada_x=float(df(x_nuevo)),
                    error_relativo=error_actual,
                )
            )"""
            return NewtonRaphsonResult(
                exito=True,
                mensaje=f"Raíz encontrada después de {iteracion + 1} iteraciones.",
                iteraciones=resultados,
                raiz=x_nuevo,
            )
        x_actual = x_nuevo
        iteracion += 1

    return NewtonRaphsonResult(
        exito=False,
        mensaje=f"No convergió después de {max_iteraciones} iteraciones. Último valor: x = {x_actual}",
        iteraciones=resultados,
        raiz=None,
    )