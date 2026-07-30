# Capa PLANTILLA: Interfaz de usuario por consola para gestionar aprendices
import re

PATRON_LETRAS = r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+"
PATRON_CORREO = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"
TIPOS_DOC_VALIDOS = ("CC", "TI", "CE")


# ------------------------------------------------------------------
# Punto 2: Validaciones de entrada reutilizables y claras
# ------------------------------------------------------------------

def _leer_no_vacio(mensaje):
    """Pide un dato que no puede quedar en blanco."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("⚠️  Este campo no puede estar vacío. Intenta de nuevo.")


def _leer_solo_letras(mensaje):
    """Pide un dato que solo debe contener letras y espacios (ej: nombres, programa)."""
    while True:
        valor = _leer_no_vacio(mensaje)
        if re.fullmatch(PATRON_LETRAS, valor):
            return valor.title()
        print("⚠️  Este campo solo debe contener letras. Intenta de nuevo.")


def _leer_solo_numeros(mensaje):
    """Pide un dato que solo debe contener números (ej: documento, ficha)."""
    while True:
        valor = _leer_no_vacio(mensaje)
        if valor.isdigit():
            return valor
        print("⚠️  Este campo solo debe contener números. Intenta de nuevo.")


def _leer_tipo_documento(mensaje):
    """Pide el tipo de documento y valida que sea una opción permitida."""
    while True:
        valor = _leer_no_vacio(mensaje).upper()
        if valor in TIPOS_DOC_VALIDOS:
            return valor
        print(f"⚠️  Tipo de documento no válido. Opciones: {', '.join(TIPOS_DOC_VALIDOS)}.")


def _leer_correo(mensaje):
    """Pide un correo electrónico y valida su formato (usuario@dominio.com)."""
    while True:
        valor = _leer_no_vacio(mensaje).lower()
        if re.fullmatch(PATRON_CORREO, valor):
            return valor
        print("⚠️  Correo electrónico no válido. Ejemplo: nombre@correo.com")


# --- Versiones "opcionales" usadas al editar: Enter = conservar el valor actual ---

def _leer_opcional_letras(mensaje, actual):
    valor = input(mensaje).strip()
    while valor and not re.fullmatch(PATRON_LETRAS, valor):
        print("⚠️  Este campo solo debe contener letras. Intenta de nuevo.")
        valor = input(mensaje).strip()
    return valor.title() if valor else actual


def _leer_opcional_numeros(mensaje, actual):
    valor = input(mensaje).strip()
    while valor and not valor.isdigit():
        print("⚠️  Este campo solo debe contener números. Intenta de nuevo.")
        valor = input(mensaje).strip()
    return valor if valor else actual


def _leer_opcional_correo(mensaje, actual):
    valor = input(mensaje).strip().lower()
    while valor and not re.fullmatch(PATRON_CORREO, valor):
        print("⚠️  Correo electrónico no válido. Ejemplo: nombre@correo.com")
        valor = input(mensaje).strip().lower()
    return valor if valor else actual


# ------------------------------------------------------------------
# Entradas de datos
# ------------------------------------------------------------------

def obtener_datos_aprendiz():
    """Solicita al usuario los datos para registrar un aprendiz, validando cada campo."""
    tipo_doc = _leer_tipo_documento("Tipo de documento (CC/TI/CE): ")
    documento = _leer_solo_numeros("Número de documento: ")
    nombres = _leer_solo_letras("Nombres: ")
    apellidos = _leer_solo_letras("Apellidos: ")
    ficha = _leer_solo_numeros("Número de Ficha: ")
    programa = _leer_solo_letras("Programa de Formación: ")
    correo = _leer_correo("Correo electrónico: ")

    return {
        "tipo_doc": tipo_doc,
        "documento": documento,
        "nombres": nombres,
        "apellidos": apellidos,
        "ficha": ficha,
        "programa": programa,
        "correo": correo,
    }


def obtener_documento(mensaje="Número de documento: "):
    """Solicita un número de documento para buscar, editar o eliminar un aprendiz."""
    return _leer_solo_numeros(mensaje)


def obtener_datos_actualizacion(actual):
    """Solicita los nuevos datos para editar un aprendiz.
    Si el usuario deja el campo vacío, se conserva el valor actual."""
    print("\n(Deja el campo vacío y presiona Enter para mantener el valor actual)")

    nombres = _leer_opcional_letras(f"Nombres [{actual['nombres']}]: ", actual["nombres"])
    apellidos = _leer_opcional_letras(f"Apellidos [{actual['apellidos']}]: ", actual["apellidos"])
    ficha = _leer_opcional_numeros(f"Número de Ficha [{actual['ficha']}]: ", actual["ficha"])
    programa = _leer_opcional_letras(f"Programa de Formación [{actual['programa']}]: ", actual["programa"])
    correo = _leer_opcional_correo(f"Correo electrónico [{actual.get('correo', '')}]: ", actual.get("correo", ""))

    return {
        "nombres": nombres,
        "apellidos": apellidos,
        "ficha": ficha,
        "programa": programa,
        "correo": correo,
    }


def obtener_busqueda():
    """Solicita el texto a buscar (nombre o ficha)."""
    return _leer_no_vacio("Ingresa el nombre o el número de ficha a buscar: ")


def confirmar_eliminacion(nombre):
    """Pide confirmación antes de eliminar un aprendiz."""
    respuesta = input(f"¿Seguro que deseas eliminar a {nombre}? (s/n): ").strip().lower()
    return respuesta == "s"


# ------------------------------------------------------------------
# Salidas / mensajes
# ------------------------------------------------------------------

def mostrar_mensaje(mensaje):
    iconos = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"{iconos.get(mensaje['type'], '')} {mensaje['text']}")


def mostrar_aprendiz(aprendiz):
    """Muestra los datos de un único aprendiz."""
    print(
        f"Documento: {aprendiz['documento']} ({aprendiz['tipo_doc']}), "
        f"Nombres: {aprendiz['nombres']}, Apellidos: {aprendiz['apellidos']}, "
        f"Ficha: {aprendiz['ficha']}, "
        f"Programa: {aprendiz['programa']}, Correo: {aprendiz.get('correo', 'N/A')}"
    )


def mostrar_lista_aprendices(aprendices):
    """Muestra la lista de aprendices registrados."""
    if not aprendices:
        print("No hay aprendices registrados.")
        return

    print("\n--- Lista de Aprendices ---")
    for aprendiz in aprendices:
        mostrar_aprendiz(aprendiz)


# ------------------------------------------------------------------
# Punto 7: Menú principal
# ------------------------------------------------------------------

def mostrar_menu_principal():
    print("\n===== Sistema de Registro de Aprendices SENA =====")
    print("1. Registrar aprendiz")
    print("2. Editar aprendiz")
    print("3. Eliminar aprendiz")
    print("4. Buscar aprendiz (por nombre o ficha)")
    print("5. Ver lista completa")
    print("6. Exportar lista a CSV")
    print("0. Salir")


def obtener_opcion_menu():
    opciones_validas = ("0", "1", "2", "3", "4", "5", "6")
    while True:
        opcion = input("Selecciona una opción: ").strip()
        if opcion in opciones_validas:
            return opcion
        print("⚠️  Opción no válida. Intenta de nuevo.")
