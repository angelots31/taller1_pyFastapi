"""
Pruebas para src/models/trainee_model.py

Cada prueba redirige ARCHIVO_DATOS y ARCHIVO_CSV a un directorio temporal (tmp_path)
para no tocar nunca los datos reales del proyecto (data/aprendices.json),
y reinicia la lista en memoria antes de cada caso.
"""
import csv
import json

import pytest

from models import trainee_model


@pytest.fixture(autouse=True)
def datos_temporales(tmp_path, monkeypatch):
    """Aísla cada prueba: redirige los archivos de datos a una carpeta temporal
    y deja la lista en memoria vacía antes de cada prueba."""
    monkeypatch.setattr(trainee_model, "DIRECTORIO_DATOS", str(tmp_path))
    monkeypatch.setattr(trainee_model, "ARCHIVO_DATOS", str(tmp_path / "aprendices.json"))
    monkeypatch.setattr(trainee_model, "ARCHIVO_CSV", str(tmp_path / "aprendices.csv"))
    monkeypatch.setattr(trainee_model, "aprendices", [])
    yield


def aprendiz_ejemplo(documento="123", nombres="Ander", apellidos="Flor"):
    return {
        "tipo_doc": "CC",
        "documento": documento,
        "nombres": nombres,
        "apellidos": apellidos,
        "ficha": "111111",
        "programa": "Adso",
        "correo": "ander@correo.com",
    }


# --------------------------------------------------------------
# registrar_aprendiz / obtener_todos
# --------------------------------------------------------------

def test_registrar_aprendiz_nuevo_se_agrega_y_persiste():
    aprendiz = aprendiz_ejemplo()

    resultado = trainee_model.registrar_aprendiz(aprendiz)

    assert resultado is True
    assert trainee_model.obtener_todos() == [aprendiz]

    # Se debe haber guardado en el archivo JSON
    with open(trainee_model.ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        guardado = json.load(f)
    assert guardado == [aprendiz]


def test_registrar_aprendiz_documento_duplicado_no_se_agrega():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="123"))

    resultado = trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="123", nombres="Otro", apellidos="Nombre"))

    assert resultado is False
    assert len(trainee_model.obtener_todos()) == 1


# --------------------------------------------------------------
# buscar_por_documento
# --------------------------------------------------------------

def test_buscar_por_documento_encuentra_existente():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="123"))

    encontrado = trainee_model.buscar_por_documento("123")

    assert encontrado is not None
    assert encontrado["documento"] == "123"


def test_buscar_por_documento_no_encuentra_inexistente():
    assert trainee_model.buscar_por_documento("999") is None


# --------------------------------------------------------------
# buscar_por_nombre_o_ficha
# --------------------------------------------------------------

def test_buscar_por_nombre_o_ficha_por_nombre_parcial_e_insensible_a_mayusculas():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="1", nombres="Ander", apellidos="Flor"))
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="2", nombres="Maria", apellidos="Ruiz"))

    resultados = trainee_model.buscar_por_nombre_o_ficha("ander")

    assert len(resultados) == 1
    assert resultados[0]["documento"] == "1"


def test_buscar_por_nombre_o_ficha_por_ficha():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="1"))

    resultados = trainee_model.buscar_por_nombre_o_ficha("111111")

    assert len(resultados) == 1


def test_buscar_por_nombre_o_ficha_sin_coincidencias_retorna_lista_vacia():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="1"))

    resultados = trainee_model.buscar_por_nombre_o_ficha("no existe")

    assert resultados == []


# --------------------------------------------------------------
# actualizar_aprendiz
# --------------------------------------------------------------

def test_actualizar_aprendiz_existente_actualiza_datos():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="123", nombres="Nombre", apellidos="Viejo"))

    resultado = trainee_model.actualizar_aprendiz("123", {"nombres": "Nombre", "apellidos": "Nuevo"})

    assert resultado is True
    actualizado = trainee_model.buscar_por_documento("123")
    assert actualizado["apellidos"] == "Nuevo"
    # El documento no debe cambiar
    assert actualizado["documento"] == "123"


def test_actualizar_aprendiz_inexistente_retorna_false():
    resultado = trainee_model.actualizar_aprendiz("999", {"nombres": "Nadie", "apellidos": "Nadie"})

    assert resultado is False


# --------------------------------------------------------------
# eliminar_aprendiz
# --------------------------------------------------------------

def test_eliminar_aprendiz_existente_lo_elimina():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="123"))

    resultado = trainee_model.eliminar_aprendiz("123")

    assert resultado is True
    assert trainee_model.buscar_por_documento("123") is None
    assert trainee_model.obtener_todos() == []


def test_eliminar_aprendiz_inexistente_retorna_false():
    resultado = trainee_model.eliminar_aprendiz("999")

    assert resultado is False


# --------------------------------------------------------------
# exportar_a_csv
# --------------------------------------------------------------

def test_exportar_a_csv_genera_archivo_con_encabezado_y_filas():
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="1", nombres="Ander", apellidos="Flor"))
    trainee_model.registrar_aprendiz(aprendiz_ejemplo(documento="2", nombres="Maria", apellidos="Ruiz"))

    ruta = trainee_model.exportar_a_csv()

    with open(ruta, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    assert len(filas) == 2
    assert filas[0]["documento"] == "1"
    assert filas[1]["apellidos"] == "Ruiz"


# --------------------------------------------------------------
# _cargar_datos (carga inicial desde archivo)
# --------------------------------------------------------------

def test_cargar_datos_archivo_inexistente_retorna_lista_vacia():
    assert trainee_model._cargar_datos() == []


def test_cargar_datos_archivo_corrupto_retorna_lista_vacia(tmp_path, monkeypatch):
    archivo_corrupto = tmp_path / "corrupto.json"
    archivo_corrupto.write_text("{ esto no es json valido ", encoding="utf-8")
    monkeypatch.setattr(trainee_model, "ARCHIVO_DATOS", str(archivo_corrupto))

    assert trainee_model._cargar_datos() == []
