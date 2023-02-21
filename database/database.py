import os
from sqlalchemy import create_engine, desc, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from datetime import datetime
# Create the database file
database_file = './database/database.db'
if not os.path.exists(database_file):
    open(database_file, 'a').close()

# Setting up the SQLite Database with SQLAlchemy
engine = create_engine(f'sqlite:///{database_file}', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Msp(Base):
    __tablename__ = 'msp'
    id = Column(Integer, primary_key=True)
    tipo_documento = Column(String)
    pais = Column(String)
    documento = Column(String)
    nombre = Column(String)
    nacimiento = Column(String)
    departamento = Column(String)
    celular = Column(String)
    motivo = Column(String)
    tiene_sintomas = Column(Boolean)
    fecha_inicio_sintomas = Column(String)
    test = Column(String)
    fecha_toma_muestra = Column(String)
    fecha_informe = Column(String)
    resultado = Column(String)
    procedencia = Column(String)
    realizado_en = Column(String)
    created = Column(String, default=datetime.now().strftime("%d/%m/%Y"))
    uploaded = Column(Boolean, default=0)
    uploaded_date = Column(String)
    file_id = Column(String)
    wait_verification = Column(Boolean, default=0)
    __table_args__ = (UniqueConstraint('documento', 'resultado', name='_documento_resultado_uc'),)

class Nobilis(Base):
    __tablename__ = 'nobilis'
    id = Column(Integer, primary_key=True)
    idTipoDocumento = Column(String, nullable=False)
    nroDoc = Column(String, nullable=False)
    fechaNacimiento = Column(String, nullable=False)
    # estadoCivilDesc = Column(String)
    # ocupacionDesc = Column(String)
    # escolaridadDesc = Column(String)
    # escolaridadDesc = Column(String)
    domicilio = Column(String)
    # codigoPostal = Column(String)
    # localidadDesc = Column(Boolean)
    # partidoDesc = Column(String)
    # provinciaDesc = Column(Integer)
    # paisDesc = Column(String)
    telefono = Column(String)
    # celular = Column(String)
    # telefonoLaboral = Column(String)
    # celularLaboral = Column(String)
    # faxLaboral = Column(String)
    fechaAlta = Column(String)
    # domicilioLaboral = Column(String)
    localidadOrigenDesc = Column(String)
    # partidoOrigenDesc = Column(String)
    # provinciaOrigenDesc = Column(String)
    # paisOrigenDesc = Column(String)
    # lugarOrigenDesc = Column(String)
    # cuit = Column(String)
    # cuil = Column(String)
    sexo = Column(String, nullable=False) # F/M
    # generoDesc = Column(String)
    nroHistoriaClinica = Column(String, nullable=False) # Same as nroDoc
    email = Column(String)
    nombre = Column(String, nullable=False)
    # segundoNombre = Column(String)
    apellido = Column(String, nullable=False)
    # segundoApellido = Column(String)
    habilitado = Column(Boolean, default=1)
    # observaciones = Column(String)
    institucionesDesc = Column(String, nullable=False)
    planDesc = Column(String, nullable=False)
    ##### ORDEN:
    centroDesc = Column(String, nullable=False)
    origenPacienteDesc = Column(String)
    # profesionalDesc = Column(String)
    # profesionalMatricula = Column(String)
    servicioDesc = Column(String)
    locacionDesc = Column(String)
    # diagnosticoDesc = Column(String)
    # tipoFisiologicoDesc = Column(String)
    # tiempo = Column(Integer)
    urgente = Column(Boolean, default=1, nullable=False)
    autorizada = Column(Boolean, default=1, nullable=False)
    # internacion = Column(String)
    # laboratorioDesc = Column(String)
    # idExterno = Column(String)
    # observacion = Column(String)
    # internacionDesc = Column(String)
    ordenPendiente = Column(Boolean, default=0, nullable=False)
    prescripcionMedica = Column(String)
    # programacionDesc = Column(String)
    # sectorizacionDesc = Column(String)
    estudios = Column(String, nullable=False)
    file_id = Column(String)
    uploaded = Column(Boolean, default=0)
    uploaded_date = Column(String)
    created = Column(String, default=datetime.now().strftime("%d/%m/%Y"))
    error = Column(Boolean, default=0)
    error_desc = Column(String)
    
class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    platform = Column(String) # MSP or NOBILIS
    file_id = Column(String)
    created = Column(String, default=datetime.now().strftime("%d/%m/%Y"))
    data_count = Column(Integer)
    
Base.metadata.create_all(engine)
