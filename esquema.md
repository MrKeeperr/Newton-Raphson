proyecto-newton-raphson/
├── .gitignore                  <- Ignora node_modules, __pycache__, entornos virtuales, etc.
├── README.md                   <- Documentación vital: cómo instalar y correr el proyecto.
├── docker-compose.yml          <- (Opcional pero recomendado) Para levantar ambos servicios con un solo comando.
│
├── api/                        <- Tu backend en FastAPI (Python)
│   ├── requirements.txt        <- Dependencias (fastapi, uvicorn, sympy para las derivadas, etc.)
│   ├── main.py                 <- Punto de entrada de la API y configuración de CORS.
│   ├── core/
│   │   └── config.py           <- Configuraciones generales de la API.
│   ├── models/
│   │   └── schemas.py          <- Modelos de Pydantic (ej. RequestEcuacion, ResponseIteracion).
│   └── services/
│       └── newton_raphson.py   <- ¡El corazón del proyecto! Aquí va la lógica matemática pura.
│
└── frontend/                   <- Tu aplicación web en Svelte (JavaScript/HTML/CSS)
    ├── package.json            <- Dependencias de Node.js y scripts (dev, build).
    ├── vite.config.js          <- Configuración del empaquetador (Vite viene por defecto con Svelte).
    ├── index.html              <- El archivo HTML principal.
    ├── public/                 <- Favicon y recursos estáticos.
    └── src/
        ├── main.js             <- Punto de entrada de Svelte.
        ├── App.svelte          <- Componente principal que coordina la vista.
        ├── lib/                <- Componentes reutilizables.
        │   ├── FormularioEcuacion.svelte  <- Input para la función, x0 y tolerancia.
        │   └── TablaResultados.svelte     <- Renderiza las iteraciones y el error relativo.
        └── assets/             <- Estilos globales (CSS) o imágenes.