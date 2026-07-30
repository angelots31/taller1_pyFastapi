import json
import os
import csv

# --- Punto 1: Ruta del archivo JSON dentro de la carpeta data/ ---
# Se calcula de forma dinámica para que funcione sin importar desde dónde
# se ejecute el programa (no se deja "quemada" una ruta fija).
DIRECTORIO_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIRECTORIO_DATOS = os.path.join(DIRECTORIO_BASE, "data")
ARCHIVO_DATOS = os.path.join(DIRECTORIO_DATOS, "aprendices.json")
ARCHIVO_CSV = os.path.join(DIRECTORIO_DATOS, "aprendices.csv")


def _cargar_datos():
    """Carga la lista de aprendices desde el archivo JSON. Si no existe, retorna una lista vacía."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (json.JSONDecodeError, OSError):
        # Si el archivo está corrupto o no se puede leer, se inicia con lista vacía
        return []


def _guardar_datos(datos):
    """Guarda la lista de aprendices en el archivo JSON."""
    os.makedirs(DIRECTORIO_DATOS, exist_ok=True)
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# Lista de aprendices, se carga una sola vez al iniciar el programa
aprendices = _cargar_datos()


def obtener_todos():
    """Obtiene todos los aprendices registrados."""
    return aprendices


def buscar_por_documento(documento):
    """Busca un aprendiz por su número de documento."""
    for a in aprendices:
        if a["documento"] == documento:
            return a
    return None


def buscar_por_nombre_o_ficha(consulta):
    """Busca aprendices cuyo nombre completo (nombres + apellidos) o ficha
    coincidan (parcialmente) con el texto dado."""
    consulta = consulta.strip().lower()
    resultados = []
    for a in aprendices:
        nombre_completo = f"{a['nombres']} {a['apellidos']}".lower()
        if consulta in nombre_completo or consulta in a["ficha"].lower():
            resultados.append(a)
    return resultados


def registrar_aprendiz(nuevo_aprendiz):
    """Registra un nuevo aprendiz si no existe previamente."""
    if buscar_por_documento(nuevo_aprendiz["documento"]):
        return False  # Ya existe un aprendiz con este documento
    aprendices.append(nuevo_aprendiz)
    _guardar_datos(aprendices)
    return True


def actualizar_aprendiz(documento, nuevos_datos):
    """Actualiza los datos de un aprendiz ya existente. No permite cambiar el documento."""
    existente = buscar_por_documento(documento)
    if not existente:
        return False
    existente.update(nuevos_datos)
    _guardar_datos(aprendices)
    return True


def eliminar_aprendiz(documento):
    """Elimina un aprendiz de la lista según su número de documento."""
    existente = buscar_por_documento(documento)
    if not existente:
        return False
    aprendices.remove(existente)
    _guardar_datos(aprendices)
    return True


def exportar_a_csv():
    """Exporta la lista de aprendices a un archivo CSV dentro de la carpeta data/."""
    os.makedirs(DIRECTORIO_DATOS, exist_ok=True)
    campos = ["tipo_doc", "documento", "nombres", "apellidos", "ficha", "programa", "correo"]

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for aprendiz in aprendices:
            escritor.writerow(aprendiz)

    return ARCHIVO_CSV
