from views import trainee_view
from templates import trainee_template


def principal():
    while True:
        # Punto 7: Menú principal con todas las opciones disponibles
        trainee_template.mostrar_menu_principal()
        opcion = trainee_template.obtener_opcion_menu()

        if opcion == "1":
            trainee_view.registrar_aprendiz_vista()
        elif opcion == "2":
            trainee_view.editar_aprendiz_vista()
        elif opcion == "3":
            trainee_view.eliminar_aprendiz_vista()
        elif opcion == "4":
            trainee_view.buscar_aprendiz_vista()
        elif opcion == "5":
            trainee_view.estado_vista()
        elif opcion == "6":
            trainee_view.exportar_csv_vista()
        elif opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break


if __name__ == "__main__":
    principal()
