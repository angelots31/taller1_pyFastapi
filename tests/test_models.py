"""
Pruebas para src/models/trainee_model.py

Cada prueba redirige DATA_FILE y CSV_FILE a un directorio temporal (tmp_path)
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
    monkeypatch.setattr(trainee_model, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(trainee_model, "DATA_FILE", str(tmp_path / "aprendices.json"))
    monkeypatch.setattr(trainee_model, "CSV_FILE", str(tmp_path / "aprendices.csv"))
    monkeypatch.setattr(trainee_model, "trainee", [])
    yield

def aprendiz_ejemplo(documento="123", nombre="Ander Flor"):
    return {
        "tipo_doc": "CC",
        "documento": documento,
        "nombre": nombre,
        "ficha": "111111",
        "programa": "Adso",
        "correo": "ander@correo.com",
    }

# --------------------------------------------------------------
# register_trainee / get_all
# --------------------------------------------------------------

def test_register_trainee_nuevo_se_agrega_y_persiste():
    aprendiz = aprendiz_ejemplo()

    resultado = trainee_model.register_trainee(aprendiz)

    assert resultado is True
    assert trainee_model.get_all() == [aprendiz]

    # Se debe haber guardado en el archivo JSON
    with open(trainee_model.DATA_FILE, "r", encoding="utf-8") as f:
        guardado = json.load(f)
    assert guardado == [aprendiz]


def test_register_trainee_documento_duplicado_no_se_agrega():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="123"))

    resultado = trainee_model.register_trainee(aprendiz_ejemplo(documento="123", nombre="Otro Nombre"))

    assert resultado is False
    assert len(trainee_model.get_all()) == 1


# --------------------------------------------------------------
# search_by_document
# --------------------------------------------------------------

def test_search_by_document_encuentra_existente():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="123"))

    encontrado = trainee_model.search_by_document("123")

    assert encontrado is not None
    assert encontrado["documento"] == "123"


def test_search_by_document_no_encuentra_inexistente():
    assert trainee_model.search_by_document("999") is None


# --------------------------------------------------------------
# search_by_name_or_group
# --------------------------------------------------------------

def test_search_by_name_or_group_por_nombre_parcial_e_insensible_a_mayusculas():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="1", nombre="Ander Flor"))
    trainee_model.register_trainee(aprendiz_ejemplo(documento="2", nombre="Maria Ruiz"))

    resultados = trainee_model.search_by_name_or_group("ander")

    assert len(resultados) == 1
    assert resultados[0]["documento"] == "1"


def test_search_by_name_or_group_por_ficha():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="1"))

    resultados = trainee_model.search_by_name_or_group("111111")

    assert len(resultados) == 1


def test_search_by_name_or_group_sin_coincidencias_retorna_lista_vacia():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="1"))

    resultados = trainee_model.search_by_name_or_group("no existe")

    assert resultados == []


# --------------------------------------------------------------
# update_trainee
# --------------------------------------------------------------

def test_update_trainee_existente_actualiza_datos():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="123", nombre="Nombre Viejo"))

    resultado = trainee_model.update_trainee("123", {"nombre": "Nombre Nuevo"})

    assert resultado is True
    actualizado = trainee_model.search_by_document("123")
    assert actualizado["nombre"] == "Nombre Nuevo"
    # El documento no debe cambiar
    assert actualizado["documento"] == "123"


def test_update_trainee_inexistente_retorna_false():
    resultado = trainee_model.update_trainee("999", {"nombre": "Nadie"})

    assert resultado is False


# --------------------------------------------------------------
# delete_trainee
# --------------------------------------------------------------

def test_delete_trainee_existente_lo_elimina():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="123"))

    resultado = trainee_model.delete_trainee("123")

    assert resultado is True
    assert trainee_model.search_by_document("123") is None
    assert trainee_model.get_all() == []


def test_delete_trainee_inexistente_retorna_false():
    resultado = trainee_model.delete_trainee("999")

    assert resultado is False


# --------------------------------------------------------------
# export_to_csv
# --------------------------------------------------------------

def test_export_to_csv_genera_archivo_con_encabezado_y_filas():
    trainee_model.register_trainee(aprendiz_ejemplo(documento="1", nombre="Ander Flor"))
    trainee_model.register_trainee(aprendiz_ejemplo(documento="2", nombre="Maria Ruiz"))

    ruta = trainee_model.export_to_csv()

    with open(ruta, "r", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    assert len(filas) == 2
    assert filas[0]["documento"] == "1"
    assert filas[1]["nombre"] == "Maria Ruiz"


# --------------------------------------------------------------
# _load_data (carga inicial desde archivo)
# --------------------------------------------------------------

def test_load_data_archivo_inexistente_retorna_lista_vacia():
    assert trainee_model._load_data() == []


def test_load_data_archivo_corrupto_retorna_lista_vacia(tmp_path, monkeypatch):
    archivo_corrupto = tmp_path / "corrupto.json"
    archivo_corrupto.write_text("{ esto no es json valido ", encoding="utf-8")
    monkeypatch.setattr(trainee_model, "DATA_FILE", str(archivo_corrupto))

    assert trainee_model._load_data() == []
