# 📘 Sistema de Registro de Aprendices SENA

Proyecto en Python para la gestión de aprendices SENA mediante interfaz por consola, organizado en capas **Model / View / Template**. Los archivos y carpetas mantienen sus nombres originales en inglés, pero todas las funciones y variables dentro del código están en español.

## ✨ Funcionalidades

El menú principal permite:

1. **Registrar aprendiz** — pide tipo de documento, número de documento, nombre completo, ficha, programa y correo, con validación de cada campo.
2. **Editar aprendiz** — busca por documento y permite actualizar nombre, ficha, programa y correo (dejar en blanco conserva el valor actual).
3. **Eliminar aprendiz** — busca por documento y pide confirmación antes de borrar.
4. **Buscar aprendiz** — por nombre (coincidencia parcial) o número de ficha.
5. **Ver lista completa** — muestra todos los aprendices registrados.
6. **Exportar a CSV** — genera `data/aprendices.csv` a partir de los datos actuales.
0. Salir.

> **Nota:** el nombre se maneja como un solo campo (`nombre completo`), no separado en nombres/apellidos.

## 🗂️ Estructura del proyecto

```
python_tercer_tri/
│
├── src/
│   ├── main.py                  # Punto de entrada de la aplicación
│   │
│   ├── models/
│   │   └── trainee_model.py     # Capa MODEL: persistencia en JSON, CRUD, export a CSV
│   │
│   ├── views/
│   │   └── trainee_view.py      # Capa VIEW: lógica de negocio, conecta model y template
│   │
│   └── templates/
│       └── trainee_template.py  # Capa TEMPLATE: entrada/salida por consola, validaciones
│
├── data/
│   ├── aprendices.json          # Fuente de datos persistente
│   └── aprendices.csv           # Generado por la opción "Exportar a CSV"
│
├── tests/
│   ├── test_models.py           # Pruebas de la capa MODEL
│   └── test_views.py            # Pruebas de la capa VIEW
│
├── conftest.py                  # Permite que pytest resuelva los imports de src/
├── pytest.ini                   # Configuración de pytest
├── .gitignore
├── README.md
└── requirements.txt              # Dependencias (pytest)
```

## ▶️ Cómo ejecutar

Desde la carpeta `src/`:

```bash
py src/main.py
```

## ✅ Cómo correr las pruebas

Desde la raíz del proyecto (donde está `pytest.ini`):

```bash
py -m pip install -r requirements.txt
py -m pytest -v
```
