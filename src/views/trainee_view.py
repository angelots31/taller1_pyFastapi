from models import trainee_model
from templates import trainee_template

def register_trainee_view():

    data = trainee_template.get_trainee_input()

    if trainee_model.search_by_document(data["documento"]):
        trainee_template.display_message(
            {
                "type": "error",
                "text": "Ya existe un aprendiz registrado con este número de documento.",
            }
        )
        return

    trainee_model.register_trainee(data)

    trainee_template.display_message(
        {
            "type": "success",
            "text": f"Aprendiz {data['nombre']} registrado exitosamente en la ficha {data['ficha']}.",
        }
    )

def status_view():
    all_trainees = trainee_model.get_all()
    trainee_template.display_trainee_list(all_trainees)

def edit_trainee_view():
    document = trainee_template.get_document_input(
        "Número de documento del aprendiz a editar: "
    )
    current = trainee_model.search_by_document(document)

    if not current:
        trainee_template.display_message(
            {"type": "error", "text": "No existe un aprendiz con ese número de documento."}
        )
        return

    trainee_template.display_message({"type": "info", "text": "Datos actuales del aprendiz:"})
    trainee_template.display_trainee(current)

    new_data = trainee_template.get_trainee_update_input(current)
    trainee_model.update_trainee(document, new_data)

    trainee_template.display_message(
        {"type": "success", "text": f"Aprendiz {new_data['nombre']} actualizado exitosamente."}
    )

def delete_trainee_view():
    document = trainee_template.get_document_input(
        "Número de documento del aprendiz a eliminar: "
    )
    current = trainee_model.search_by_document(document)

    if not current:
        trainee_template.display_message(
            {"type": "error", "text": "No existe un aprendiz con ese número de documento."}
        )
        return

    trainee_template.display_trainee(current)

    if not trainee_template.display_confirm_delete(current["nombre"]):
        trainee_template.display_message({"type": "info", "text": "Eliminación cancelada."})
        return

    trainee_model.delete_trainee(document)
    trainee_template.display_message(
        {"type": "success", "text": "Aprendiz eliminado exitosamente."}
    )

def search_trainee_view():
    query = trainee_template.get_search_query()
    resultados = trainee_model.search_by_name_or_group(query)

    if not resultados:
        trainee_template.display_message(
            {"type": "info", "text": "No se encontraron aprendices que coincidan con la búsqueda."}
        )
        return

    trainee_template.display_trainee_list(resultados)


def export_csv_view():
    all_trainees = trainee_model.get_all()

    if not all_trainees:
        trainee_template.display_message(
            {"type": "info", "text": "No hay aprendices registrados para exportar."}
        )
        return

    ruta = trainee_model.export_to_csv()
    trainee_template.display_message(
        {"type": "success", "text": f"Lista exportada exitosamente en: {ruta}"}
    )
