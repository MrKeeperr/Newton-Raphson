from pydantic import BaseModel, Field
from typing import Optional, List


class NewtonRaphsonRequest(BaseModel):
    """
    esquema de request para el cálculo de Newton-Raphson.
    Recibe los datos de entrada del formulario del frontend.
    """

    funcion: str = Field(
        ...,
        description="Funcion matematica como texto (e.g., 'x**2 - 4', 'sin(x) - x/2')",
        min_length=1,
        examples=["x**2 - 4", "cos(x) - x", "x**3 - 2*x - 5"],
    )

    x0: float = Field(
        ...,
        description="Punto inicial (x₀) para comenzar la iteración de Newton-Raphson",
        examples=[1.0, 2.5, -1.0],
    )

    tolerancia: float = Field(
        default=0.0001,
        description="Tolerancia para el error relativo para detener las iteraciones",
        gt=0,
        examples=[0.0001, 1e-6, 0.01],
    )

    max_iteraciones: Optional[int] = Field(
        default=50,
        description="Número máximo de iteraciones permitidas (por defecto: 50)",
        gt=0,
        le=100,
    )


class NewtonRaphsonResponse(BaseModel):
    """
    esquema de response para el cálculo de Newton-Raphson.
    Devuelve el resultado de la raíz encontrada, el número de iteraciones realizadas,
    """

    paso: int = Field(default=0, description="Número de iteración")

    x_actual: float = Field(..., description="Valor actual de x en la iteración")

    f_x: float = Field(..., description="Valor de la función evaluada en x_actual")

    f_derivada_x: float = Field(
        ..., description="Valor de la derivada de la función evaluada en x_actual"
    )

    error_relativo: Optional[float] = Field(
        None,
        description="Error relativo entre x_actual y la raíz encontrada (si se ha encontrado una raíz)",
    )


class NewtonRaphsonResult(BaseModel):
    """
    Esquema de resultado final para el cálculo de Newton-Raphson.
    """

    exito: bool = Field(..., description="Indica si el método fallo o convergió")

    mensaje: str = Field(
        ...,
        description="Mensaje descriptivo del resultado (e.g., 'Raíz encontrada', 'No se encontró raíz dentro de las iteraciones permitidas')",
        examples=[
            "Raíz encontrada",
            "No se encontró raíz dentro de las iteraciones permitidas",
            "Error: derivada cero en x_actual",
        ],
    )

    iteraciones: List[NewtonRaphsonResponse] = Field(
        ..., description="Lista de todas las iteraciones realizadas"
    )

    raiz: Optional[float] = Field(
        None, description="Valor de la raíz encontrada (si se ha encontrado una raíz)"
    )
