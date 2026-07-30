# 📘 Título y descripción
## Sistema de Registro de Aprendices SENA
Proyecto en Python para la gestión de aprendices SENA mediante interfaz por consola.

1. Registrar la siguiente información mediante una función.
* Tipo doc
* Documento
* Nombres
* Apellidos
* Ficha
* Programa

# 🗂️ Estructructa del Proyecto 

taller1_pyfastapi/
│
├── src/
│   ├── main.py              # Punto de entrada de la aplicación
│   │
│   ├── models/              # Capa MODEL: Datos, esquemas y lógica de persistencia
│   │   └── aprendiz_model.py
│   │
│   ├── views/               # Capa VIEW: Lógica de negocio y manejo de peticiones
│   │   └── aprendiz_view.py
│   │
│   └── templates/           # Capa TEMPLATE: Formato de salida / Interfaces / Consola
│       └── aprendiz_template.py
│
├── data/
│   └── aprendices.json      # Fuente de datos persistente
│
├── tests/
│   ├── test_models.py       # Pruebas para la capa de modelos
│   └── test_views.py        # Pruebas para la lógica de vistas
│
├── .gitignore               # Archivos ignorados por Git
├── README.md                # Documentación del proyecto
└── requirements.txt         # Dependencias (FastAPI, Uvicorn, Pydantic, etc.)