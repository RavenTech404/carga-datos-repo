from zeep import Client
from handlers.nobilis import update_upload_state_nobilis, update_error_state_nobilis
import random
from tkinter import messagebox
class CargaNobilis:
    def __init__(self, data):
        for element in data:
            # Codigos de respuesta: 202 = OK | 953 = NOT OK
            if self.cargar_paciente(element)['codigo'] == 202:
                if self.cargar_orden(element)['codigo'] == 202:
                    try:
                        update_upload_state_nobilis(element['nroDoc'], element['created'], 1, element['file_id'])
                    except Exception as e:
                        print("DATABASE ERROR:", e)
                else:
                    # Error en orden
                    try:
                        update_error_state_nobilis(
                            element['nroDoc'], 
                            element['created'], 
                            1, 
                            'order', 
                            element['file_id'])
                        messagebox.showerror("Error en cargar orden", f"{self.cargar_orden(element)['msg']}")
                    except Exception as e:
                        print("DATABASE ERROR:", e)
            else:
                if self.update_paciente(element)['codigo'] == 202:
                    if self.cargar_orden(element)['codigo'] == 202:
                        try:
                            update_upload_state_nobilis(element['nroDoc'], element['created'], 1, element['file_id'])
                        except Exception as e:
                            print("DATABASE ERROR:", e)
                    else:
                        # Error en orden
                        try:
                            update_error_state_nobilis(
                                element['nroDoc'], 
                                element['created'], 
                                1, 
                                'order', 
                                element['file_id'])
                            messagebox.showerror("Error en cargar orden", f"{self.cargar_orden(element)['msg']}")
                        except Exception as e:
                            print("DATABASE ERROR:", e)
                else:
                    # Error en paciente
                    try:
                        update_error_state_nobilis(
                            element['nroDoc'], 
                            element['created'], 
                            1, 
                            'paciente', 
                            element['file_id'])
                        messagebox.showerror("Error en cargar paciente", f"{self.update_paciente(element)['msg']}")
                    except Exception as e:
                        print("DATABASE ERROR:", e)
    
    def cargar_paciente(self, data):
        # Replace with the actual WSDL service URL
        wsdl_url = ''
        
        # Create a client object to interact with the service
        client = Client(wsdl_url)

        # Create a dictionary with the patient's information
        paciente = {
            'id': '?',
            'idTipoDocumento': '?',
            'nroDoc': '?',
            'fechaNacimiento': '?',
            'estadoCivilDesc': '?',
            'ocupacionDesc': '?',
            'escolaridadDesc': '?',
            'escolaridadDesc': '?',
            'domicilio': '?',
            'codigoPostal': '?',
            'localidadDesc': '?',
            'partidoDesc': '?',
            'provinciaDesc': '?',
            'paisDesc': '?',
            'telefono': '?',
            'celular': '?',
            'telefonoLaboral': '?',
            'celularLaboral': '?',
            'faxLaboral': '?',
            'fechaAlta': '?',
            'domicilioLaboral': '?',
            'localidadOrigenDesc': '?',
            'partidoOrigenDesc': '?',
            'provinciaOrigenDesc': '?',
            'paisOrigenDesc': '?',
            'lugarOrigenDesc': '?',
            'cuit': '?',
            'cuil': '?',
            'sexo': '?',
            'generoDesc': '?',
            'nroHistoriaClinica': '?',
            'email': '?',
            'nombre': '?',
            'segundoNombre': '?',
            'apellido': '?',
            'segundoApellido': '?',
            'habilitado': '?',
            'observaciones': '?',
            'institucionesDesc': '?', 
            'planDesc': '?'
        }

        # Replace the empty strings with the actual patient's information
        paciente['idTipoDocumento'] = data['idTipoDocumento'].upper()
        paciente['nroDoc'] = data['nroDoc']
        paciente['fechaNacimiento'] = data['fechaNacimiento']
        paciente['domicilio'] = data['domicilio']
        paciente['telefono'] = data['telefono']
        paciente['fechaAlta'] = data['fechaAlta']
        paciente['localidadOrigenDesc'] = data['localidadOrigenDesc']
        paciente['sexo'] = data['sexo']
        paciente['nroHistoriaClinica'] = data['nroHistoriaClinica']
        paciente['email'] = data['email']
        paciente['nombre'] = data['nombre']
        paciente['apellido'] = data['apellido']
        paciente['habilitado'] = 'true'
        paciente['institucionesDesc'] = data['institucionesDesc']
        paciente['planDesc'] = data['planDesc']

        # Send the patient's information to the service
        response = client.service.cargarPaciente(pacientesWsdl=paciente)

        # Print the response from the service
        print(response)
        return response

    def update_paciente(self, data):
        # Replace with the actual WSDL service URL
        wsdl_url = ''
        
        # Create a client object to interact with the service
        client = Client(wsdl_url)

        # Create a dictionary with the patient's information
        paciente = {
            'id': '?',
            'idTipoDocumento': '?',
            'nroDoc': '?',
            'fechaNacimiento': '?',
            'estadoCivilDesc': '?',
            'ocupacionDesc': '?',
            'escolaridadDesc': '?',
            'escolaridadDesc': '?',
            'domicilio': '?',
            'codigoPostal': '?',
            'localidadDesc': '?',
            'partidoDesc': '?',
            'provinciaDesc': '?',
            'paisDesc': '?',
            'telefono': '?',
            'celular': '?',
            'telefonoLaboral': '?',
            'celularLaboral': '?',
            'faxLaboral': '?',
            'fechaAlta': '?',
            'domicilioLaboral': '?',
            'localidadOrigenDesc': '?',
            'partidoOrigenDesc': '?',
            'provinciaOrigenDesc': '?',
            'paisOrigenDesc': '?',
            'lugarOrigenDesc': '?',
            'cuit': '?',
            'cuil': '?',
            'sexo': '?',
            'generoDesc': '?',
            'nroHistoriaClinica': '?',
            'email': '?',
            'nombre': '?',
            'segundoNombre': '?',
            'apellido': '?',
            'segundoApellido': '?',
            'habilitado': '?',
            'observaciones': '?',
            'institucionesDesc': '?', 
            'planDesc': '?'
        }

        # Replace the empty strings with the actual patient's information
        paciente['idTipoDocumento'] = data['idTipoDocumento'].upper()
        paciente['nroDoc'] = data['nroDoc']
        paciente['fechaNacimiento'] = data['fechaNacimiento']
        paciente['domicilio'] = data['domicilio']
        paciente['telefono'] = data['telefono']
        paciente['fechaAlta'] = data['fechaAlta']
        paciente['localidadOrigenDesc'] = data['localidadOrigenDesc']
        paciente['sexo'] = data['sexo']
        paciente['nroHistoriaClinica'] = data['nroHistoriaClinica']
        paciente['email'] = data['email']
        paciente['nombre'] = data['nombre']
        paciente['apellido'] = data['apellido']
        paciente['habilitado'] = 'true'
        paciente['institucionesDesc'] = data['institucionesDesc']
        paciente['planDesc'] = data['planDesc']

        # Send the patient's information to the service
        response = client.service.actualizarDatosPaciente(pacientesWsdl=paciente)

        # Print the response from the service
        print(f"Paciente:\n{paciente}")
        print(response)
        return response

    def cargar_orden(self, data):
        # Replace with the actual WSDL service URL
        wsdl_url = ''
        
        # Create a client object to interact with the service
        client = Client(wsdl_url)

        # Create a dictionary with the patient's information
        orden = {
        'centroDesc': '?',
        'origenPacienteDesc': '?',
        'profesionalDesc': '?',
        'profesionalMatricula': '?',
        'nroHistClinica': '?',
        'servicioDesc': '?',
        'locacionDesc': '?',
        'diagnosticoDesc': '?',
        'tipoFisiologicoDesc': '?',
        'tiempo': '?',
        'urgente': '?',
        'autorizada':'?',
        'internacion':'?',
        'laboratorioDesc':'?',
        'idExterno':'?',
        'observacion':'?',
        'internacionDesc':'?',
        'ordenPendiente':'?',
        'institucionDesc':'?',
        'planDesc':'?',
        'prescripcionMedica':'?',
        'programacionDesc':'?',
        'sectorizacionDesc':'?',
        'estudios':'?',
        }

        orden['centroDesc'] = data['centroDesc']
        orden['origenPacienteDesc'] = data['origenPacienteDesc'] 
        orden['nroHistClinica'] = data['nroHistoriaClinica']
        orden['servicioDesc'] = data['servicioDesc']
        orden['urgente'] = 0
        # orden['autorizada'] = 1
        orden['ordenPendiente'] = 0
        #orden['planDesc'] = data['planDesc']
        #orden['prescripcionMedica'] = data['prescripcionMedica']
        orden['locacionDesc'] = data['locacionDesc']
        orden['estudios'] = int(data['estudios'])
        orden['idExterno'] = random.randint(0, 99999999999999)

        #print(orden)
        # Send the patient's information to the service
        response = client.service.cargarOrden(ordenesWsdl=orden)
        print(f"orden:\n{orden}")
        # Print the response from the service
        print(response)
        return response

# RESPONSE CODES:

# {
#     'codigo': 953,
#     'msg': 'Ya existe el número de historia clinica que desea crear.'
# }

# {
#     'codigo': 202,
#     'msg': 'El paciente fue dado de alta correctamente.'
# }

# {
#     'codigo': 901,
#     'msg': 'El centro 112 no fue dado de alta en Nobilis.'
# }