import re

PATRON_LETRAS = r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+"
PATRON_CORREO = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"
TIPOS_DOC_VALIDOS = ("CC", "TI", "CE")

def _leer_no_vacio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("⚠️ Este campo no puede estar vacío. Intenta de nuevo.")

def _leer_solo_letras(mensaje):
    while True:
        valor = _leer_no_vacio(mensaje)
        if re.fullmatch(PATRON_LETRAS, valor):
            return valor.title()
        print("⚠️ Este campo solo debe contener letras. Intenta de nuevo.")

def _leer_solo_numeros(mensaje):
    while True:
        valor = _leer_no_vacio(mensaje)
        if valor.isdigit():
            return valor
        print("⚠️ Este campo solo debe contener números. Intenta de nuevo.")

def _leer_tipo_documento(mensaje):
    while True:
        valor = _leer_no_vacio(mensaje).upper()
        if valor in TIPOS_DOC_VALIDOS:
            return valor
        print(f"⚠️ Tipo de documento no válido. Opciones: {', '.join(TIPOS_DOC_VALIDOS)}.")


def _leer_correo(mensaje):
    while True:
        valor = _leer_no_vacio(mensaje).lower()
        if re.fullmatch(PATRON_CORREO, valor):
            return valor
        print("⚠️ Correo electrónico no válido. Ejemplo: nombre@correo.com")

def _leer_opcional_letras(mensaje, actual):
    valor = input(mensaje).strip()
    while valor and not re.fullmatch(PATRON_LETRAS, valor):
        print("⚠️ Este campo solo debe contener letras. Intenta de nuevo.")
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

def get_trainee_input():
    type_id = _leer_tipo_documento("Tipo de documento (CC/TI/CE): ")
    id = _leer_solo_numeros("Número de documento: ")
    name = _leer_solo_letras("Nombre completo: ")
    group_code = _leer_solo_numeros("Número de Ficha: ")
    program = _leer_solo_letras("Programa de Formación: ")
    email = _leer_correo("Correo electrónico: ")

    return {
        "tipo_doc": type_id,
        "documento": id,
        "nombre": name,
        "ficha": group_code,
        "programa": program,
        "correo": email,
    }

def get_document_input(mensaje="Número de documento: "):
    return _leer_solo_numeros(mensaje)


def get_trainee_update_input(current):
    print("\n(Deja el campo vacío y presiona Enter para mantener el valor actual)")

    name = _leer_opcional_letras(f"Nombre completo [{current['nombre']}]: ", current["nombre"])
    group_code = _leer_opcional_numeros(f"Número de Ficha [{current['ficha']}]: ", current["ficha"])
    program = _leer_opcional_letras(f"Programa de Formación [{current['programa']}]: ", current["programa"])
    email = _leer_opcional_correo(f"Correo electrónico [{current.get('correo', '')}]: ", current.get("correo", ""))

    return {
        "nombre": name,
        "ficha": group_code,
        "programa": program,
        "correo": email,
    }

def get_search_query():
    return _leer_no_vacio("Ingresa el nombre o el número de ficha a buscar: ")

def display_confirm_delete(nombre):
    respuesta = input(f"¿Seguro que deseas eliminar a {nombre}? (s/n): ").strip().lower()
    return respuesta == "s"

def display_message(message):
    icons = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"{icons.get(message['type'], '')} {message['text']}")

def display_trainee(trai):
    print(
        f"Documento: {trai['documento']} ({trai['tipo_doc']}), "
        f"Nombre: {trai['nombre']}, Ficha: {trai['ficha']}, "
        f"Programa: {trai['programa']}, Correo: {trai.get('correo', 'N/A')}"
    )

def display_trainee_list(trainee):
    if not trainee:
        print("No hay aprendices registrados.")
        return

    print("\n--- Lista de Aprendices ---")
    for trai in trainee:
        display_trainee(trai)

def display_main_menu():
    print("\n===== Sistema de Registro de Aprendices SENA =====")
    print("1. Registrar aprendiz")
    print("2. Editar aprendiz")
    print("3. Eliminar aprendiz")
    print("4. Buscar aprendiz (por nombre o ficha)")
    print("5. Ver lista completa")
    print("6. Exportar lista a CSV")
    print("0. Salir")

def get_menu_option():
    opciones_validas = ("0", "1", "2", "3", "4", "5", "6")
    while True:
        opcion = input("Selecciona una opción: ").strip()
        if opcion in opciones_validas:
            return opcion
        print("⚠️ Opción no válida. Intenta de nuevo.")
