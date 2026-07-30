from models import trainee_model
from templates import trainee_template


def registrar_aprendiz_vista():
    """Lógica para procesar el registro de un aprendiz desde la vista."""
    # Solicitar datos al usuario a través de la capa PLANTILLA
    datos = trainee_template.obtener_datos_aprendiz()

    # Validar si el aprendiz ya existe
    if trainee_model.buscar_por_documento(datos["documento"]):
        trainee_template.mostrar_mensaje(
            {
                "type": "error",
                "text": "Ya existe un aprendiz registrado con este número de documento.",
            }
        )
        return

    # Registrar aprendiz a través de la capa MODELO
    trainee_model.registrar_aprendiz(datos)

    # Confirmar en la interfaz
    trainee_template.mostrar_mensaje(
        {
            "type": "success",
            "text": f"Aprendiz {datos['nombres']} {datos['apellidos']} registrado exitosamente en la ficha {datos['ficha']}.",
        }
    )


def estado_vista():
    """Muestra el estado actual de la lista de aprendices registrados."""
    todos_los_aprendices = trainee_model.obtener_todos()
    trainee_template.mostrar_lista_aprendices(todos_los_aprendices)


def editar_aprendiz_vista():
    """Lógica para editar los datos de un aprendiz existente."""
    documento = trainee_template.obtener_documento(
        "Número de documento del aprendiz a editar: "
    )
    actual = trainee_model.buscar_por_documento(documento)

    if not actual:
        trainee_template.mostrar_mensaje(
            {"type": "error", "text": "No existe un aprendiz con ese número de documento."}
        )
        return

    trainee_template.mostrar_mensaje({"type": "info", "text": "Datos actuales del aprendiz:"})
    trainee_template.mostrar_aprendiz(actual)

    nuevos_datos = trainee_template.obtener_datos_actualizacion(actual)
    trainee_model.actualizar_aprendiz(documento, nuevos_datos)

    trainee_template.mostrar_mensaje(
        {"type": "success", "text": f"Aprendiz {nuevos_datos['nombres']} {nuevos_datos['apellidos']} actualizado exitosamente."}
    )


def eliminar_aprendiz_vista():
    """Lógica para eliminar un aprendiz existente de la lista."""
    documento = trainee_template.obtener_documento(
        "Número de documento del aprendiz a eliminar: "
    )
    actual = trainee_model.buscar_por_documento(documento)

    if not actual:
        trainee_template.mostrar_mensaje(
            {"type": "error", "text": "No existe un aprendiz con ese número de documento."}
        )
        return

    trainee_template.mostrar_aprendiz(actual)

    if not trainee_template.confirmar_eliminacion(f"{actual['nombres']} {actual['apellidos']}"):
        trainee_template.mostrar_mensaje({"type": "info", "text": "Eliminación cancelada."})
        return

    trainee_model.eliminar_aprendiz(documento)
    trainee_template.mostrar_mensaje(
        {"type": "success", "text": "Aprendiz eliminado exitosamente."}
    )


def buscar_aprendiz_vista():
    """Lógica para buscar aprendices por nombre o ficha."""
    consulta = trainee_template.obtener_busqueda()
    resultados = trainee_model.buscar_por_nombre_o_ficha(consulta)

    if not resultados:
        trainee_template.mostrar_mensaje(
            {"type": "info", "text": "No se encontraron aprendices que coincidan con la búsqueda."}
        )
        return

    trainee_template.mostrar_lista_aprendices(resultados)


def exportar_csv_vista():
    """Lógica para exportar la lista de aprendices a un archivo CSV."""
    todos_los_aprendices = trainee_model.obtener_todos()

    if not todos_los_aprendices:
        trainee_template.mostrar_mensaje(
            {"type": "info", "text": "No hay aprendices registrados para exportar."}
        )
        return

    ruta = trainee_model.exportar_a_csv()
    trainee_template.mostrar_mensaje(
        {"type": "success", "text": f"Lista exportada exitosamente en: {ruta}"}
    )
