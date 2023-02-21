## Variables:
url = "" # <-- Poner la url entre comillas
# Login
usuario_path = "/html/body/form/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div[2]/div/div/input"
contraseña_path = "/html/body/form/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div[3]/div/div/input"
usuario_verificar = ""
usuario = ""
contraseña = ""
boton_path = "/html/body/form/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div[3]/div/input"
# Direcciones WEB:
menu_cargar_resultados = "/html/body/div[1]/header/div[2]/div/button"
boton_cargar_resultados = "/html/body/form/div[1]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[3]/a"

# Step 1
tipo_documento = '//*[@id="vTIPODOCUMENTOCODIGO"]' # Select
pais = "//*[@id='vPAISCODIGO']" # Select
nro_documento = '//*[@id="vREGISTRONRODOCUMENTO"]' # Text
consultar_datos_boton = '//*[@id="CONSULTARDATOS"]'
# Step 2
p_nombre = "//*[@id='vRESULTADOPACPRIMERNOMBRE']" # text
s_nombre = '//*[@id="vRESULTADOPACSEGUNDONOMBRE"]' # text
p_apellido = '//*[@id="vRESULTADOPACPRIMERAPELLIDO"]' # text
s_apellido = '//*[@id="vRESULTADOPACSEGUNDOAPELLIDO"]' # text
nacimiento = '//*[@id="vRESULTADOPACDOB"]' # date
departamento = '//*[@id="vDEPARTAMENTOID"]' # select
prestador_del_paciente = '//*[@id="vRESULTADOPACPRESTADORID"]'  # select
quien_solicita_test = '//*[@id="vQUIENSOLICITA"]' # select
celular = '//*[@id="vRESULTADOPACCELULAR"]' # text
motivo = '//*[@id="vRESULTADOMOTIVO"]' # select
# Tiene sintomas?
tiene_sintomas = '//*[@id="vRESULTADOSINTOMAS"]' # select
fecha_inicio_sintomas = '//*[@id="vRESULTADOFECHASINTOMAS"]' # date
# #
tipo_de_test = '//*[@id="vRESULTADOTIPOTEST"]' # select
fecha_toma_muestra = "//*[@id='vAUX_RESULTADOFECHAMUESTRA']" # date
fecha_resultado = "//*[@id='vAUX_RESULTADOFECHA']" # date 
menu_cargar_resultado = '//*[@id="vRESULTADOVALOR"]' # select
donde_se_realizo = '//*[@id="vRESULTADOLUGARDONDEREALIZATEST"]' # select
boton_insertar_resultados = "//*[@id='CARGARRESULTADO']"
boton_nuevo_resultado = "//*[@id='CANCELAR']"

web_elements_first_stage = [
    tipo_documento,
    pais,nro_documento,
    ]
web_elements_second_stage = [
    p_nombre,
    s_nombre,
    p_apellido,
    s_apellido,
    nacimiento,
    departamento,
    prestador_del_paciente,
    quien_solicita_test,
    celular,
    motivo,
    tiene_sintomas,
    fecha_inicio_sintomas,
    tipo_de_test,
    fecha_toma_muestra,
    fecha_resultado,
    menu_cargar_resultado,
    donde_se_realizo,
    boton_insertar_resultados,
]