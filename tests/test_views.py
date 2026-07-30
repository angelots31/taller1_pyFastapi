"""
Pruebas para src/views/trainee_view.py

La vista delega en las capas MODELO y PLANTILLA, así que aquí no probamos
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
    "nombres": "Ander",
    "apellidos": "Flor",
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
        trainee_template, "mostrar_mensaje", lambda msg: capturados.append(msg)
    )
    return capturados


# --------------------------------------------------------------
# registrar_aprendiz_vista
# --------------------------------------------------------------

def test_registrar_aprendiz_vista_aprendiz_nuevo_lo_registra(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_datos_aprendiz", lambda: APRENDIZ)
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: None)
    llamadas = []
    monkeypatch.setattr(
        trainee_model, "registrar_aprendiz", lambda datos: llamadas.append(datos) or True
    )

    trainee_view.registrar_aprendiz_vista()

    assert llamadas == [APRENDIZ]
    assert mensajes[-1]["type"] == "success"


def test_registrar_aprendiz_vista_documento_duplicado_no_registra(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_datos_aprendiz", lambda: APRENDIZ)
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: APRENDIZ)
    llamado = []
    monkeypatch.setattr(
        trainee_model, "registrar_aprendiz", lambda datos: llamado.append(datos)
    )

    trainee_view.registrar_aprendiz_vista()

    assert llamado == []  # nunca se debe llegar a registrar
    assert mensajes[-1]["type"] == "error"


# --------------------------------------------------------------
# estado_vista
# --------------------------------------------------------------

def test_estado_vista_muestra_todos_los_aprendices(monkeypatch):
    monkeypatch.setattr(trainee_model, "obtener_todos", lambda: [APRENDIZ])
    recibido = []
    monkeypatch.setattr(
        trainee_template, "mostrar_lista_aprendices", lambda lista: recibido.append(lista)
    )

    trainee_view.estado_vista()

    assert recibido == [[APRENDIZ]]


# --------------------------------------------------------------
# editar_aprendiz_vista
# --------------------------------------------------------------

def test_editar_aprendiz_vista_documento_inexistente_muestra_error(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_documento", lambda msg: "999")
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: None)

    trainee_view.editar_aprendiz_vista()

    assert mensajes[-1]["type"] == "error"


def test_editar_aprendiz_vista_documento_existente_actualiza(monkeypatch, mensajes):
    nuevos_datos = {"nombres": "Nombre", "apellidos": "Editado", "ficha": "111111",
                     "programa": "Adso", "correo": "nuevo@correo.com"}

    monkeypatch.setattr(trainee_template, "obtener_documento", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "mostrar_aprendiz", lambda a: None)
    monkeypatch.setattr(trainee_template, "obtener_datos_actualizacion", lambda actual: nuevos_datos)
    llamadas = []
    monkeypatch.setattr(
        trainee_model,
        "actualizar_aprendiz",
        lambda doc, datos: llamadas.append((doc, datos)) or True,
    )

    trainee_view.editar_aprendiz_vista()

    assert llamadas == [("123", nuevos_datos)]
    assert mensajes[-1]["type"] == "success"


# --------------------------------------------------------------
# eliminar_aprendiz_vista
# --------------------------------------------------------------

def test_eliminar_aprendiz_vista_documento_inexistente_muestra_error(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_documento", lambda msg: "999")
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: None)

    trainee_view.eliminar_aprendiz_vista()

    assert mensajes[-1]["type"] == "error"


def test_eliminar_aprendiz_vista_confirmado_elimina(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_documento", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "mostrar_aprendiz", lambda a: None)
    monkeypatch.setattr(trainee_template, "confirmar_eliminacion", lambda nombre: True)
    llamadas = []
    monkeypatch.setattr(
        trainee_model, "eliminar_aprendiz", lambda doc: llamadas.append(doc) or True
    )

    trainee_view.eliminar_aprendiz_vista()

    assert llamadas == ["123"]
    assert mensajes[-1]["type"] == "success"


def test_eliminar_aprendiz_vista_cancelado_no_elimina(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_documento", lambda msg: "123")
    monkeypatch.setattr(trainee_model, "buscar_por_documento", lambda doc: APRENDIZ)
    monkeypatch.setattr(trainee_template, "mostrar_aprendiz", lambda a: None)
    monkeypatch.setattr(trainee_template, "confirmar_eliminacion", lambda nombre: False)
    llamado = []
    monkeypatch.setattr(trainee_model, "eliminar_aprendiz", lambda doc: llamado.append(doc))

    trainee_view.eliminar_aprendiz_vista()

    assert llamado == []
    assert mensajes[-1]["type"] == "info"


# --------------------------------------------------------------
# buscar_aprendiz_vista
# --------------------------------------------------------------

def test_buscar_aprendiz_vista_con_resultados_los_muestra(monkeypatch):
    monkeypatch.setattr(trainee_template, "obtener_busqueda", lambda: "ander")
    monkeypatch.setattr(trainee_model, "buscar_por_nombre_o_ficha", lambda q: [APRENDIZ])
    recibido = []
    monkeypatch.setattr(
        trainee_template, "mostrar_lista_aprendices", lambda lista: recibido.append(lista)
    )

    trainee_view.buscar_aprendiz_vista()

    assert recibido == [[APRENDIZ]]


def test_buscar_aprendiz_vista_sin_resultados_muestra_info(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_template, "obtener_busqueda", lambda: "nadie")
    monkeypatch.setattr(trainee_model, "buscar_por_nombre_o_ficha", lambda q: [])

    trainee_view.buscar_aprendiz_vista()

    assert mensajes[-1]["type"] == "info"


# --------------------------------------------------------------
# exportar_csv_vista
# --------------------------------------------------------------

def test_exportar_csv_vista_sin_aprendices_no_exporta(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_model, "obtener_todos", lambda: [])
    llamado = []
    monkeypatch.setattr(trainee_model, "exportar_a_csv", lambda: llamado.append(True))

    trainee_view.exportar_csv_vista()

    assert llamado == []
    assert mensajes[-1]["type"] == "info"


def test_exportar_csv_vista_con_aprendices_exporta(monkeypatch, mensajes):
    monkeypatch.setattr(trainee_model, "obtener_todos", lambda: [APRENDIZ])
    monkeypatch.setattr(trainee_model, "exportar_a_csv", lambda: "/ruta/falsa/aprendices.csv")

    trainee_view.exportar_csv_vista()

    assert mensajes[-1]["type"] == "success"
    assert "/ruta/falsa/aprendices.csv" in mensajes[-1]["text"]
