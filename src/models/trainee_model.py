import json
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "aprendices.json")
CSV_FILE = os.path.join(DATA_DIR, "aprendices.csv")


def _load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            contenido = file.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (json.JSONDecodeError, OSError):
        return []

def _save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

trainee = _load_data()

def get_all():
    return trainee

def search_by_document(document):
    for a in trainee:
        if a["documento"] == document:
            return a
    return None

def search_by_name_or_group(query):
    query = query.strip().lower()
    resultados = []
    for a in trainee:
        if query in a["nombre"].lower() or query in a["ficha"].lower():
            resultados.append(a)
    return resultados

def register_trainee(new_trainee):
    if search_by_document(new_trainee["documento"]):
        return False 
    trainee.append(new_trainee)
    _save_data(trainee)
    return True

def update_trainee(document, new_data):
    existing = search_by_document(document)
    if not existing:
        return False
    existing.update(new_data)
    _save_data(trainee)
    return True

def delete_trainee(document):
    existing = search_by_document(document)
    if not existing:
        return False
    trainee.remove(existing)
    _save_data(trainee)
    return True

def export_to_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    campos = ["tipo_doc", "documento", "nombre", "ficha", "programa", "correo"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        for aprendiz in trainee:
            writer.writerow(aprendiz)

    return CSV_FILE