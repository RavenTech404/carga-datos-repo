from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from tkinter import messagebox
import time
from variables import *
from config import *
from database.database import *
import json
from handlers.msp import update_upload_state_msp, name_handler

class ManageBrowser:
    def __init__(self, payload):
        self.payload = payload
        if len(payload) > 0:
            print("manage browser init")
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            #self.driver.set_window_size(320, 480)
            self.driver.get(url)
            time.sleep(2)
            self.signin()

    def signin(self):
        # función para loguear usuario
        try:
            # busca input de user y escribe el usuario designado
            self.driver.find_element(By.XPATH, usuario_path).send_keys(usuario)
            # busca input de pass y escribe la contrasena designado
            self.driver.find_element(By.XPATH, contraseña_path).send_keys(contraseña)
            # busca botón e ingresa
            self.driver.find_element(By.XPATH, boton_path).click()
            print("Logged in!")
            time.sleep(3)
        except Exception as e:
            print("Already logged in or error: " , e)

    def insertar_datos(self):
        url_registro_resultado = "https://servicios.coronavirus.gub.uy/AgendaLabBackend/servlet/com.agendalab.registroresultado"
        self.driver.get(url_registro_resultado)
        # If is data in payload, run
        if len(self.payload) > 0: 
            # Catch if element's not uploaded
            element_counter = 0
            object_waiting_verification = {}
            # If site is available
            for element in self.payload:
                object_waiting_verification = element
                print(f"object_waiting_verification: {object_waiting_verification}")
                # Check for site availability
                # If site second stage is available
                print('documento', element['Documento'], 'nombre', element['Nombre'])
                if self.first_stage(element) == True:
                    self.second_stage(element)
                    try:    
                        # Check si el insertado de datos es controlado por el usuario
                        if CONTROLADO == True:
                            response = messagebox.askyesno(
                                title="Insertar datos", 
                                message="Desea insertar los datos ingresados en el formulario?"
                                )
                            if response:
                                try:
                                    self.driver.find_element(By.XPATH, boton_insertar_resultados).click()
                                    update_upload_state_msp(str(element['Documento']), datetime.now().strftime("%d/%m/%Y"), 1,str(element['file_id']))
                                    print("datos insertados")
                                except Exception as e:
                                    print(f"PUPPET ERROR:\nHa habido un error al subir del paciente:{str(element['Documento'])}\n\nDetalles de error:\n{e}")
                                    time.sleep(6)
                            else:
                                response_continue = messagebox.askyesno(
                                    title="Insertar datos", 
                                    message="Si desea continuar con el siguiente presione 'Si' para salir presione 'No'?"
                                )
                                if response_continue:
                                    self.driver.find_element(By.XPATH, boton_nuevo_resultado).click()
                                    time.sleep(3)
                                    continue
                                else:
                                    self.close()
                                    break
                        else:
                            try:
                                self.driver.find_element(By.XPATH, boton_insertar_resultados).click()
                                update_upload_state_msp(str(element['Documento']), datetime.now().strftime("%d/%m/%Y"), 1,str(element['file_id']))
                                print("datos insertados")
                            except Exception as e:
                                print(f"PUPPET ERROR:\nHa habido un error al subir del paciente:{str(element['Documento'])}\n\nDetalles de error:\n{e}")
                                time.sleep(6)
                                
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", f"{e}")
                        # Si hay un error y no es el primer usuario subido
                        # es por que el anterior usuario no se subió correctamente
                        # es necesario modificar la DB para especificar que no ha sido subido.
                        if element_counter > 0:
                            try:
                                update_upload_state_msp(
                                    object_waiting_verification['Documento'],
                                    datetime.now().strftime("%d/%m/%Y"),
                                    0,
                                    str(element['file_id'])
                                )
                            except Exception as e:
                                print("Closed before entering data")

    def first_stage(self, element):
        for web_element in web_elements_first_stage:
            self.check_site_availability(web_element)
        try:
            # Tipo de documento
            Select(self.driver.find_element(By.XPATH, tipo_documento)).select_by_visible_text(element['Tipo de documento'])
            # Pais
            Select(self.driver.find_element(By.XPATH, pais)).select_by_visible_text(f" {element['Pais']}")
            # Documento
            self.driver.find_element(By.XPATH, nro_documento).send_keys(str(element['Documento']))
            time.sleep(1)
            if self.driver.find_element(By.XPATH, nro_documento).get_attribute('value') == str(element['Documento']):
                time.sleep(2)
                return True
            else:
                return False
        except Exception as e:
            print(e)


    def second_stage(self, element):
        nombre_completo = json.loads(name_handler(element['Nombre']))
        while not self.driver.find_element(By.XPATH, nro_documento).get_attribute('value') == str(element['Documento']):
            self.first_stage(element)

        self.click_consultar_datos(consultar_datos_boton, element)
        time.sleep(1)
        # Checking second stage
        for web_element in web_elements_second_stage:
            self.check_site_availability(web_element)
        # Nombre
        self.driver.find_element(By.XPATH, p_nombre).send_keys(nombre_completo['primer_nombre'])
        self.driver.find_element(By.XPATH, s_nombre).send_keys(nombre_completo['segundo_nombre'])
        self.driver.find_element(By.XPATH, p_apellido).send_keys(nombre_completo['primer_apellido'])
        self.driver.find_element(By.XPATH, s_apellido).send_keys(nombre_completo['segundo_apellido'])
        # Fecha nacimiento
        self.driver.find_element(By.XPATH, nacimiento).send_keys(element['Fecha de nacimiento'])
        # Departamento
        Select(self.driver.find_element(By.XPATH, departamento)).select_by_visible_text(element['Departamento'])
        # Procedencia
        try:
            if element['Procedencia'].upper() != "NINGUNA":
                Select(self.driver.find_element(By.XPATH, prestador_del_paciente)).select_by_visible_text(element['Procedencia'].upper())
        except Exception as e:
            print(e)
        # Quien Solicita
        Select(self.driver.find_element(By.XPATH, quien_solicita_test)).select_by_visible_text('Particular')
        # Celular
        phone = self.driver.find_element(By.XPATH, celular).get_attribute("value")
        phone if phone != "" else self.driver.find_element(By.XPATH, celular).send_keys(element['Celular'])
        # Motivo
        Select(self.driver.find_element(By.XPATH, motivo)).select_by_visible_text(element['Motivo'] if element['Motivo'] != '' else "Control")
        # Tiene sintomas
        Select(self.driver.find_element(By.XPATH, tiene_sintomas)).select_by_visible_text('SI' if element['Tiene sintomas'] == 1 else 'NO')
        # Fecha inicio sintomas
        self.driver.find_element(By.XPATH, fecha_inicio_sintomas).send_keys(element['Fecha inicio sintomas'])
        # Tipo de test
        Select(self.driver.find_element(By.XPATH, tipo_de_test)).select_by_visible_text(element['Test'])
        # Resultado (Positivo/Negativo)
        Select(self.driver.find_element(By.XPATH, menu_cargar_resultado)).select_by_visible_text(element['Resultado'])
        # Donde se realizo
        Select(self.driver.find_element(By.XPATH, donde_se_realizo)).select_by_visible_text(element['Realizado en'])
        # Fechas
        self.driver.find_element(By.XPATH, fecha_toma_muestra).send_keys(element['Fecha toma de muestra'])
        self.driver.find_element(By.XPATH, fecha_resultado).send_keys(element['Fecha informe'])  

    def check_site_availability(self, selenium_element):
        self.site_available = False
        while not self.site_available:
            print(f"Checking availability of element: {selenium_element}")
            try:
                self.driver.find_element(By.XPATH, selenium_element)
                self.site_available = True
                print(f"Element {selenium_element} is available")
            except Exception as e:
                print(f"Error in checking availability:\n{e}")
                self.site_available = False
                time.sleep(3)


    def click_consultar_datos(self, selenium_element, data):
        self.site_available = False
        while self.driver.find_element(By.XPATH, nro_documento).get_attribute('value') == str(data['Documento']):
            print(f"Checking 'consultar datos' button: {selenium_element}")
            try:
                element = self.driver.find_element(By.XPATH, selenium_element)
                element.click()
                time.sleep(3)
                break
            except Exception as e:
                print("Button not clickable:", e)

    def await_for_site_availability(self, selenium_element):
        tries = 3
        sleep = 2 
        for i in range(0, tries):
            if len(selenium_element) > 0:
                self.site_available = True
                print("Button is present on the page")
                break
            else:
                time.sleep(sleep)
                sleep += 1
        if self.site_available == False:
            messagebox.showerror("Error en el sitio", "Parece que el sitio no esta disponible, prueba nuevamente en unos minutos.")
            print("Button is not present on the page")
            self.close()

    def hide_elements(self):
        # locate the element
        element = self.driver.find_element(By.CLASS_NAME, "btn btn-default K2BToolsButton_MainAction")
        # hide the element
        self.driver.execute_script("arguments[0].style.display = 'none';", element)

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            print(e)

