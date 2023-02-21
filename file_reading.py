import pandas as pd
from tkinter import messagebox
from datetime import timedelta, datetime
import uuid

class ReadFile:
    def __init__(self, file, platform):
        if platform == 'MSP':
            self.file_to_msp(file)
        else:
            self.file_to_nobilis(file)

    def file_to_msp(self, file):
        from handlers.msp import insert_data_msp, insert_file_msp
        # Generate a random UUID for the file_id
        file_uuid = uuid.uuid4()
        # Read Excel
        df = pd.read_excel(file)
        data_count = 0
        # Read File and process data
        for i in range(0, len(df)):
            try:
                # Fecha toma muestra
                if isinstance(df['Fecha toma muestra'][i], str) == True:
                    fecha_toma_muestra_str = df['Fecha toma muestra'][i]
                    # convert the string to a datetime object
                    fecha_toma_muestra_format = datetime.strptime(fecha_toma_muestra_str, '%d/%m/%Y')  
                    # perform the subtraction
                    fecha_inicio_sintomas_calc = fecha_toma_muestra_format + timedelta(days=-2)
                    fecha_toma_muestra = fecha_toma_muestra_format.strftime("%d/%m/%Y")
                    fecha_inicio_sintomas = fecha_inicio_sintomas_calc.strftime("%d/%m/%Y")
                else:
                    fecha_toma_muestra = df['Fecha toma muestra'][i].strftime("%d/%m/%Y")
                    fecha_inicio_sintomas_calc = df['Fecha toma muestra'][i] + timedelta(days = -2)
                    fecha_inicio_sintomas = fecha_inicio_sintomas_calc.strftime("%d/%m/%Y")

                # Fecha de nacimiento
                if isinstance(df['Fecha de nacimiento'][i], str) == True:
                    fecha_de_nacimiento_format = datetime.strptime(df['Fecha de nacimiento'][i], '%d/%m/%Y')
                    fecha_de_nacimiento_format.strftime("%d/%m/%Y")
                else:
                    fecha_de_nacimiento = df['Fecha de nacimiento'][i].strftime("%d/%m/%Y")
                
                # Fecha informe
                if isinstance(df['Fecha informe'][i], str) == True:
                    fecha_de_informe_format = datetime.strptime(df['Fecha informe'][i], '%d/%m/%Y')
                    fecha_de_informe = fecha_de_informe_format.strftime("%d/%m/%Y")
                else:
                    fecha_de_informe = df['Fecha informe'][i].strftime("%d/%m/%Y")
                
                # Formatting celular
                if "/" in str(df['Celular'][i]):
                    celular = str(df['Celular'][i]).split("/")[0]
                elif ";" in str(df['Celular'][i]):
                    celular = str(df['Celular'][i]).split(";")[0]
                elif "," in str(df['Celular'][i]):
                    celular = str(df['Celular'][i]).split(",")[0]
                else:
                    celular = str(df['Celular'][i])

                data = {
                    "Tipo de documento" : 'DOCUMENTO DE IDENTIDAD (ICAO - DN)' if 'DNI' in df['Tipo de documento'][i].upper() else df['Tipo de documento'][i].upper(),
                    "Pais" : df['País'][i],
                    "Documento" : df['Documento'][i], 
                    "Nombre" : df['Nombre'][i],
                    "Fecha de nacimiento" : fecha_de_nacimiento,
                    "Departamento" : df['Departamento'][i],
                    "Celular" : celular,
                    "Motivo" : "" if 'Motivo' not in df.columns else df['Motivo'][i], 
                    "Tiene sintomas"  :  "SI",
                    "Fecha inicio de sintomas"  : fecha_inicio_sintomas, 
                    "Tipo de test" : "PCR" if "PCR" in df['Estudio'][i] else "Antígenos", 
                    "Fecha toma muestra" : fecha_toma_muestra, 
                    "Fecha de informe" : fecha_de_informe, 
                    "Resultado" : "Positivo" if "POSITIVO" in df['Resultado'][i].upper() else "Negativo",
                    "Procedencia" : df['Procedencia'][i],
                    "Donde se realizo" : "Domicilio"
                    }
                print(data)
            except Exception as e:
                print(e)
                messagebox.showerror("Error de lectura", f"Error en el renglon {i+1}. El proceso se detiene.")
            
            # INSERT Excel data rows to DB
            try:
                data_count = insert_data_msp(
                    data['Tipo de documento'], 
                    data['Pais'], 
                    str(data['Documento']), 
                    data['Nombre'], 
                    data['Fecha de nacimiento'], 
                    data['Departamento'], 
                    data['Celular'], 
                    data['Motivo'], 
                    True if data['Tiene sintomas'].upper() == "SI" else False, 
                    data['Fecha inicio de sintomas'], 
                    data['Tipo de test'], 
                    data['Fecha toma muestra'], 
                    data['Fecha de informe'], 
                    data['Resultado'], 
                    data['Procedencia'], 
                    data['Donde se realizo'],
                    file_uuid.hex
                )
                print(f"INSERT Data client, C.I: {str(data['Documento'])}")
            except Exception as e:
                print(f"Data already in DB: {str(data['Documento'])}")
        
        # INSERT Excel file to DB if data length is higher than 0
        if data_count > 0:
            try:
                insert_file_msp(file_uuid.hex)
                print(f"File: {file_uuid.hex} Inserted")
            except Exception as e:
                print("File already in DB")
        else:
            print(f"File: {file_uuid.hex} Duplicated")

    def file_to_nobilis(self, file):
        from handlers.nobilis import insert_data_nobilis, insert_file_nobilis
        # Generate a random UUID for the file_id
        file_uuid = uuid.uuid4()
        # Read Excel
        df = pd.read_excel(file)
        data_count = 0
        # Read File and process data
        for i in range(0, len(df)):
            try:
                data = {
                    "idTipoDocumento" : df['Tipo de documento'][i].upper(),
                    "nroDoc" : df['nº documento'][i], 
                    "nombre" : df['1er Nombre'][i],
                    "apellido" : df['1er Apellido'][i],
                    "fechaNacimiento" : df['Fecha de nacimiento'][i].strftime("%d/%m/%Y"),
                    "localidadOrigenDesc" : df['Locación'][i],
                    "telefono" : str(df['TELEFONOS'][i]).replace(" ", "") if ";" not in str(df['TELEFONOS'][i]) else str(df['TELEFONOS'][i]).split(";")[0],
                    "domicilio" : df['Dirección'][i], 
                    "email" : df['Correo para enviar resultado'][i] if ";" not in str(df['Correo para enviar resultado'][i]) else str(df['Correo para enviar resultado'][i]).split(";")[0], 
                    # ORDEN:
                    "centroDesc" : "AMIDEVA COVID" if "UNIVERSAL" in df['Institución'][i] else "", 
                    "origenPacienteDesc"  :  df['Institución'][i],
                    "servicioDesc"  :  df['Servicio'][i], 
                    "estudios" : df['Examen'][i],
                    "locacionDesc" : df['Locación'][i],
                    "sexo": 'M' if "sexo" not in df.columns else df['sexo'][i],
                    # ORDEN/PACIENTE
                    "fechaAlta" : df['Fecha de toma de muestra'][i].strftime("%d/%m/%Y"), 
                }
            except Exception as e:
                print(e)
                messagebox.showerror("Error de lectura", f"Error en el renglon {i+1}. El proceso se detiene.")
            
            # INSERT Excel data rows to DB
            try:
                data_count = insert_data_nobilis(
                    data['idTipoDocumento'], #
                    str(data['nroDoc']), # and Historia clinica
                    data['nombre'], #
                    data['apellido'], #
                    data['fechaNacimiento'], #
                    data['localidadOrigenDesc'],
                    data['telefono'],
                    data['domicilio'],
                    data['email'],
                    data['centroDesc'], #
                    data['origenPacienteDesc'], # and institucionDesc
                    data['servicioDesc'], # and planDesc
                    int(data['estudios']),#
                    data['locacionDesc'],
                    data['fechaAlta'],
                    data['sexo'],
                    file_uuid.hex
                )
                print(f"INSERT Data client, C.I: {str(data['nroDoc'])}")
            except Exception as e:
                print(f"Data already in DB: {str(data['nroDoc'])} or ERROR:\n{e}")
        
        # INSERT Excel file to DB if data length is higher than 0
        if data_count > 0:
            try:
                insert_file_nobilis(file_uuid.hex)
                print(f"File: {file_uuid.hex} Inserted")
            except Exception as e:
                print("File already in DB")
        else:
            print(f"File: {file_uuid.hex} Duplicated")