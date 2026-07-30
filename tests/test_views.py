"""
Pruebas para src/views/trainee_view.py

La vista delega en las capas MODEL y TEMPLATE, así que aquí no probamos
input()/print() reales: reemplazamos (monkeypatch) las funciones de esas
dos capas por versiones falsas y verificamos que la vista las llame
correctamente según el escenario (aprendiz existe / no existe, etc.).
"""
import pytest

from models import trainee_model
from templates import trainee_template
from views import trainee_view


APRENDIZ = {
    "tipo_doc": "CC",
    "documento": "123",
    "nombre": "Ander Flor",
    "ficha": "111111",
    "programa": "Adso",
    "correo": "ander@correo.com",
}


@pytest.fixture
def mensajes(monkeypatch):
    """Captura todos los mensajes que la vista intenta mostrar,
    en vez de imprimirlos en consola de verdad."""
    capturados = []
    monkeypatch.setattr(
        trainee_template, "display_message", lambda msg: capturados.append(msg)
    )
    return capturados


# --------------------------------------------------------------
# register_trainee_view
# --------------------------------------------------------------

def test_register_trainee_view_aprendiz_nuevo_lo_registra(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_trainee_input", lambda: APRENDIZ)
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: None)
    llamadas = []
    monkeypatch.setattr(
        trainee_model, "register_trainee", lambda data: llamadas.append(data) or True
    )

    trainee_view.register_trainee_view()

    assert llamadas == [APRENDIZ]
    assert mensajes[-1]["type"] == "success"


def test_register_trainee_view_documento_duplicado_no_registra(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_trainee_input", lambda: APRENDIZ)
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: APRENDIZ)
    llamado = []
    monkeypatch.setattr(
        trainee_model, "register_trainee", lambda data: llamado.append(data)
    )

    trainee_view.register_trainee_view()

    assert llamado == []  # nunca se debe llegar a registrar
    assert mensajes[-1]["type"] == "error"


# --------------------------------------------------------------
# status_view
# --------------------------------------------------------------

def test_status_view_muestra_todos_los_aprendices(monkeypatch):
    monkeypatch.setattr(trainee_model, "get_all", lambda: [APRENDIZ])
    recibido = []
    monkeypatch.setattr(
        trainee_template, "display_trainee_list", lambda lista: recibido.append(lista)
    )

    trainee_view.status_view()

    assert recibido == [[APRENDIZ]]


# --------------------------------------------------------------
# edit_trainee_view
# --------------------------------------------------------------

def test_edit_trainee_view_documento_inexistente_muestra_error(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_document_input", lambda msg: "999")
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: None)

    trainee_view.edit_trainee_view()

    assert mensajes[-1]["type"] == "error"


def test_edit_trainee_view_documento_existente_actualiza(monkeypatch, mensajes):
    nuevos_datos = {"nombre": "Nombre Editado", "ficha": "111111",
                     "programa": "Adso", "correo": "nuevo@correo.com"}

    monkeypatch.setattr(trainee_template, "get_document_input", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "display_trainee", lambda a: None)
    monkeypatch.setattr(trainee_template, "get_trainee_update_input", lambda actual: nuevos_datos)
    llamadas = []
    monkeypatch.setattr(
        trainee_model,
        "update_trainee",
        lambda doc, data: llamadas.append((doc, data)) or True,
    )

    trainee_view.edit_trainee_view()

    assert llamadas == [("123", nuevos_datos)]
    assert mensajes[-1]["type"] == "success"


# --------------------------------------------------------------
# delete_trainee_view
# --------------------------------------------------------------

def test_delete_trainee_view_documento_inexistente_muestra_error(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_document_input", lambda msg: "999")
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: None)

    trainee_view.delete_trainee_view()

    assert mensajes[-1]["type"] == "error"


def test_delete_trainee_view_confirmado_elimina(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_document_input", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "display_trainee", lambda a: None)
    monkeypatch.setattr(trainee_template, "display_confirm_delete", lambda nombre: True)
    llamadas = []
    monkeypatch.setattr(
        trainee_model, "delete_trainee", lambda doc: llamadas.append(doc) or True
    )

    trainee_view.delete_trainee_view()

    assert llamadas == ["123"]
    assert mensajes[-1]["type"] == "success"


def test_delete_trainee_view_cancelado_no_elimina(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_document_input", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "search_by_document", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "display_trainee", lambda a: None)
    monkeypatch.setattr(trainee_template, "display_confirm_delete", lambda nombre: False)
    llamado = []
    monkeypatch.setattr(trainee_model, "delete_trainee", lambda doc: llamado.append(doc))

    trainee_view.delete_trainee_view()

    assert llamado == []
    assert mensajes[-1]["type"] == "info"


# --------------------------------------------------------------
# search_trainee_view
# --------------------------------------------------------------

def test_search_trainee_view_con_resultados_los_muestra(monkeypatch):
    monkeypatch.setattr(trainee_template, "get_search_query", lambda: "ander")
    monkeypatch.setattr(trainee_model, "search_by_name_or_group", lambda q: [APRENDIZ])
    recibido = []
    monkeypatch.setattr(
        trainee_template, "display_trainee_list", lambda lista: recibido.append(lista)
    )

    trainee_view.search_trainee_view()

    assert recibido == [[APRENDIZ]]


def test_search_trainee_view_sin_resultados_muestra_info(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "get_search_query", lambda: "nadie")
    monkeypatch.setattr(trainee_model, "search_by_name_or_group", lambda q: [])

    trainee_view.search_trainee_view()

    assert mensajes[-1]["type"] == "info"


# --------------------------------------------------------------
# export_csv_view
# --------------------------------------------------------------

def test_export_csv_view_sin_aprendices_no_exporta(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_model, "get_all", lambda: [])
    llamado = []
    monkeypatch.setattr(trainee_model, "export_to_csv", lambda: llamado.append(True))

    trainee_view.export_csv_view()

    assert llamado == []
    assert mensajes[-1]["type"] == "info"


def test_export_csv_view_con_aprendices_exporta(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_model, "get_all", lambda: [APRENDIZ])
    monkeypatch.setattr(trainee_model, "export_to_csv", lambda: "/ruta/falsa/aprendices.csv")

    trainee_view.export_csv_view()

    assert mensajes[-1]["type"] == "success"
    assert "/ruta/falsa/aprendices.csv" in mensajes[-1]["text"]
