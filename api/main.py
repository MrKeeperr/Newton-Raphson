from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.models.schemas import NewtonRaphsonRequest, NewtonRaphsonResult
from api.services.newton_raphson import ejecutar_newton_raphson
app = FastAPI(
    title="Newton-Raphson API",
    description="API para calcular raíces de funciones usando el método de Newton-Raphson",
    version="1.0.0",
)

# El middleware permite la comunicación entre la api y el frontend
origins = [
    "http://localhost:5173",  # Vite/Svelte server por default
    "http://localhost:3000",  
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def read_root():
    return {"message": "Newton-Raphson API está funcionando"}

@app.post("/api/calcular-raiz", response_model=NewtonRaphsonResult)
def calcular_raiz(request: NewtonRaphsonRequest) -> NewtonRaphsonResult:
    """
    Calcula la raíz de una función usando el método de Newton-Raphson.
    Recibe una función matemática en texto, un punto inicial x₀, una tolerancia
    y opcionalmente un número máximo de iteraciones.
    Retorna la lista completa de iteraciones realizadas y la raíz encontrada
    (si el método converge) o un mensaje de error en caso contrario.
    """
    try:
        resultado = ejecutar_newton_raphson(
            funcion_texto=request.funcion,
            x0=request.x0,
            tolerancia=request.tolerancia,
            max_iteraciones=request.max_iteraciones,
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al procesar la función: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
