import json
from database.database import *

def name_handler(nombre_completo):
    # print("Nombre completo:", nombre_completo)
    posible_articles_for_name = [
    "de",
    "di",
    "la",
    "el",
    "los",
    "las",
    "De",
    "Di",
    "La",
    "El",
    "Los",
    "Las"
    ]
    separations = 0
    article_in_name = ""
    article_count = 0
    article_position = []
    first_name = ""
    second_name = ""
    first_surename = ""
    second_surename = ""
    # get white spaces
    for i in nombre_completo:
        if i == " ":
            separations += 1
    # print("Separations:", separations)

    # get articles
    word_count = 0
    for word in nombre_completo.split():
        word_count += 1
        for element in posible_articles_for_name:
            if word == element:
                article_count += 1
                article_in_name += " " + word
                article_position.append(word_count)
    # print("Articles:", article_in_name)
    # print("Articles positions:", article_position)
    # print("Articles counting:", article_count)

    if separations == 1:
        first_name = nombre_completo.split(" ")[0]
        second_name = ""
        first_surename = nombre_completo.split(" ")[1]
        second_surename = ""
        
    elif separations == 2 and article_in_name == "":
        first_name = nombre_completo.split(" ")[0]
        second_name = ""
        first_surename = nombre_completo.split(" ")[1]
        second_surename = nombre_completo.split(" ")[2]

    elif separations == 2 and article_in_name != "":
        first_name = nombre_completo.split(" ")[0]
        second_name = ""
        first_surename = article_in_name.lstrip() + nombre_completo.split(article_in_name)[1]
        second_surename = ""

    elif separations == 3 and article_in_name == "":
        first_name = nombre_completo.split(" ")[0]
        second_name = nombre_completo.split(" ")[1]
        first_surename = nombre_completo.split(" ")[2]
        second_surename = nombre_completo.split(" ")[3]

    elif separations == 3 and article_in_name != "" and article_count == 1:
        first_name = nombre_completo.split(" ")[0]
        second_name = nombre_completo.split(" ")[1] if article_position[0] == 3 else "" 
        first_surename = article_in_name.lstrip() + " " + nombre_completo.split(article_in_name)[1].split(" ")[1]
        second_surename = nombre_completo.split(" ")[-1] if article_position[0] == 2 else ""

    elif separations == 3 and article_in_name != "" and article_count == 2:
        first_name = nombre_completo.split(" ")[0]
        second_name = "" 
        first_surename = article_in_name.lstrip() + " " + nombre_completo.split(article_in_name)[1].split(" ")[1]
        second_surename = ""

    elif separations == 4 and article_in_name != "" and article_count == 1:
        first_name = nombre_completo.split(" ")[0]
        second_name = nombre_completo.split(" ")[1] if article_position[0] == 3 else ""
        first_surename = article_in_name.lstrip() + " " + nombre_completo.split(article_in_name)[1].split(" ")[1]
        second_surename = nombre_completo.split(" ")[-1] if article_position[0] == 3 else ""

    elif separations == 4 and article_in_name != "" and article_count >= 2:
        first_name = nombre_completo.split(" ")[0]
        second_name = nombre_completo.split(" ")[1] if article_position[0] == 3 else ""
        first_surename = article_in_name.lstrip() + " " + nombre_completo.split(article_in_name)[1].split(" ")[1]
        second_surename = nombre_completo.split(" ")[-1] if article_position[0] == 2 else ""
    
    elif separations == 5 and article_in_name != "" and article_count >= 2:
        first_name = nombre_completo.split(" ")[0]
        second_name = nombre_completo.split(" ")[1] if article_position[0] == 3 else ""
        first_surename = article_in_name.lstrip() + " " + nombre_completo.split(article_in_name)[1].split(" ")[1]
        second_surename = nombre_completo.split(" ")[-1] if article_position[0] == 3 else ""
    # else:
    #     first_name = nombre_completo.split(" ")[0]
    #     second_name = nombre_completo.split(" ")[1]
    #     first_surename = nombre_completo.split(" ")[2]
    #     second_surename = nombre_completo.split(" ")[3]
    data = {
        "primer_nombre" : first_name,
        "segundo_nombre" : second_name,
        "primer_apellido" : first_surename,
        "segundo_apellido" : second_surename,
    }

    payload = json.dumps(data)
    return payload

def insert_data_msp(tipo_documento, pais, documento, nombre, nacimiento, departamento, celular, motivo, tiene_sintomas, fecha_inicio_sintomas, test, fecha_toma_muestra, fecha_informe, resultado, procedencia, realizado_en, file_id):
    existing_record = session.query(Msp).filter(Msp.documento == documento, Msp.resultado == resultado).first()
    if existing_record is None:
        # Add the new record
        new_upload = Msp(tipo_documento=tipo_documento, pais=pais, documento=documento, nombre=nombre, nacimiento=nacimiento, departamento=departamento, celular=celular, motivo=motivo, tiene_sintomas=tiene_sintomas, fecha_inicio_sintomas=fecha_inicio_sintomas, test=test, fecha_toma_muestra=fecha_toma_muestra, fecha_informe=fecha_informe, resultado=resultado, procedencia=procedencia, realizado_en=realizado_en, file_id=file_id)
        session.add(new_upload)
        session.commit()
        return 1
    else:
        # Handle duplicate record
        print("Record already exists")
        return 0

def get_uploads_msp():
    query = text("SELECT * FROM msp WHERE uploaded = 1")
    result = session.execute(query)
    return result

def get_pendings_by_file_msp(file_id):
    query = text(f"SELECT * FROM msp WHERE uploaded = 0 AND file_id = '{file_id}'")
    result = session.execute(query)
    return result

def get_pendings_msp():
    query = text(f"SELECT * FROM msp WHERE uploaded = 0")
    result = session.execute(query)
    return result

def update_upload_state_msp(documento, created, uploaded, file_id):
    try:
        session = Session()
        session.query(Msp).filter(Msp.documento == documento, Msp.created == created, Msp.file_id == file_id).update({Msp.uploaded: uploaded}, synchronize_session='fetch')
        session.commit()
        session.close()
        print(f"DB NOTIF:\nPaciente: {documento} actualizado correctamente")
    except Exception as e:
        print(f"DB ERROR:\nHa habido un error al actualizar el estado de subido del paciente:{str(documento)}\n\nDetalles de error:\n{e}")

def insert_file_msp(file_id):
    new_file = File(file_id=file_id, platform='msp')
    session.add(new_file)
    session.commit()

def get_last_file_id_msp():
    query = text("SELECT file_id FROM file WHERE platform = msp ORDER BY id DESC LIMIT 1")
    result = session.execute(query)
    row = [row for row in result]
    return str(row[0][0])