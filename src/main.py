from views import trainee_view
from templates import trainee_template

def main():
    while True:
        trainee_template.display_main_menu()
        opcion = trainee_template.get_menu_option()

        if opcion == "1":
            trainee_view.register_trainee_view()
        elif opcion == "2":
            trainee_view.edit_trainee_view()
        elif opcion == "3":
            trainee_view.delete_trainee_view()
        elif opcion == "4":
            trainee_view.search_trainee_view()
        elif opcion == "5":
            trainee_view.status_view()
        elif opcion == "6":
            trainee_view.export_csv_view()
        elif opcion == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()