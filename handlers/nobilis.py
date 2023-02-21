from database.database import *

def insert_data_nobilis(idTipoDocumento, nroDoc, nombre, apellido, fechaNacimiento, localidadOrigenDesc, telefono, domicilio, email, centroDesc, origenPacienteDesc, servicioDesc, estudios, locacionDesc, fechaAlta, sexo, file_id):
    existing_record = session.query(Nobilis).filter(Nobilis.nroDoc == nroDoc, Nobilis.estudios == estudios, Nobilis.fechaAlta == fechaAlta).first()
    if existing_record is None:
        # Add the new record
        new_upload = Nobilis(
            idTipoDocumento=idTipoDocumento, 
            nroDoc=nroDoc, 
            nombre=nombre, 
            apellido=apellido, 
            fechaNacimiento=fechaNacimiento, 
            localidadOrigenDesc=localidadOrigenDesc, 
            telefono=telefono, 
            domicilio=domicilio, 
            email=email, 
            centroDesc=centroDesc,
            origenPacienteDesc=origenPacienteDesc,
            institucionesDesc=origenPacienteDesc,
            servicioDesc=servicioDesc,
            planDesc=servicioDesc,
            estudios=estudios,
            locacionDesc=locacionDesc,
            fechaAlta=fechaAlta,
            sexo=sexo,
            nroHistoriaClinica=nroDoc,
            file_id=file_id
            )
        session.add(new_upload)
        session.commit()
        return 1
    else:
        # Handle duplicate record
        print("Record already exists")
        return 0

def get_uploads_nobilis():
    query = text("SELECT * FROM nobilis WHERE uploaded = 1")
    result = session.execute(query)
    return result

def get_pendings_by_file_nobilis(file_id):
    query = text(f"SELECT * FROM nobilis WHERE uploaded = 0 AND file_id = '{file_id}'")
    result = session.execute(query)
    return result

def get_pendings_nobilis():
    query = text(f"SELECT * FROM nobilis WHERE uploaded = 0")
    result = session.execute(query)
    return result

def get_errors_nobilis():
    query = text(f"SELECT * FROM nobilis WHERE error = 1")
    result = session.execute(query)
    return result

def update_upload_state_nobilis(nroDoc, created, uploaded, file_id):
    session = Session()
    session.query(Nobilis).filter(Nobilis.nroDoc == nroDoc, Nobilis.created == created, Nobilis.file_id == file_id).update({Nobilis.uploaded: uploaded}, synchronize_session='fetch')
    session.commit()
    session.close()

def update_error_state_nobilis(nroDoc, created, error, error_desc, file_id):
    session = Session()
    session.query(Nobilis).filter(Nobilis.nroDoc == nroDoc, Nobilis.created == created, Nobilis.file_id == file_id).update({Nobilis.error: error, Nobilis.error_desc: error_desc}, synchronize_session='fetch')
    session.commit()
    session.close()

def insert_file_nobilis(file_id):
    new_file = File(file_id=file_id, platform='nobilis')
    session.add(new_file)
    session.commit()

def get_last_file_id_nobilis():
    query = text("SELECT file_id FROM file WHERE platform = nobilis ORDER BY id DESC LIMIT 1")
    result = session.execute(query)
    row = [row for row in result]
    return str(row[0][0])