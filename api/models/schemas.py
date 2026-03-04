from pydantic import BaseModel, Field
from typing import Optional


class NewtonRaphsonRequest(BaseModel):
    """
    esquema 
    Request schema for Newton-Raphson calculation.
    Receives the input data from the frontend form.
    """

    funcion: str = Field(
        ...,
        description="Mathematical function as text (e.g., 'x**2 - 4', 'sin(x) - x/2')",
        min_length=1,
        examples=["x**2 - 4", "cos(x) - x", "x**3 - 2*x - 5"],
    )

    x0: float = Field(
        ...,
        description="Initial point (x₀) to start the Newton-Raphson iteration",
        examples=[1.0, 2.5, -1.0],
    )

    tolerancia: float = Field(
        ...,
        description="Tolerance for the relative error to stop iterations",
        gt=0,
        examples=[0.0001, 1e-6, 0.01],
    )

    max_iteraciones: Optional[int] = Field(
        default=100,
        description="Maximum number of iterations allowed (default: 100)",
        gt=0,
        le=1000,
    )
