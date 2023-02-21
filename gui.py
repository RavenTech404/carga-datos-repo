import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from browser_manager import ManageBrowser
from handlers.msp import get_last_file_id_msp, get_pendings_msp, get_pendings_by_file_msp
from handlers.nobilis import get_errors_nobilis, get_pendings_nobilis
from file_reading import ReadFile
from upload_to_nobilis import CargaNobilis
from database.database import Base, engine

class Gui():
    def __init__(self):
        self.status_ok = False 
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Auto MSP")

        # Create the "File" menu option
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir Excel para MSP", command=self.open_file_msp)
        self.file_menu.add_command(label="Abrir Excel para Nobilis", command=self.open_file_nobilis)

        # Create the "Ayuda" menu option
        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Ayuda", menu=self.help_menu)
        self.help_menu.add_command(label="Procedimiento", command=self.proceedure)
        self.help_menu.add_command(label="Ver archivo de ejemplo", command=self.open_sample_file)
        
        # Create the "Ayuda" menu option
        self.clean_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Limpiar", menu=self.clean_menu)
        self.clean_menu.add_command(label="Formatear de 0", command=self.clean)

        # Create the label to display "File OK" or "Wrong Format"
        self.table_label = tk.Label(self.root, text="Estado del archivo Excel:")
        self.table_label.pack(anchor='w',pady=10)

        # Create the table to display the first three rows of the Excel file
        self.table = tk.Listbox(self.root, width=self.root.winfo_screenwidth())
        self.table.pack()

        # Create the label to display "File OK" or "Wrong Format"
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=5)

        # Create the label "MSP"
        self.msp_header = tk.Label(self.root, text="MSP", font=("TkDefaultFont", 12, "bold"))
        self.msp_header.pack(pady=10)

        # Create the button to run Selenium
        self.run_button_selenium = tk.Button(self.root, text="Subir Pacientes", command=self.upload_pendings, width="30")
        self.run_button_selenium.pack(pady=5) 

        # Create the label "NOBILIS"
        self.nobilis_header = tk.Label(self.root, text="NOBILIS", font=("TkDefaultFont", 12, "bold"))
        self.nobilis_header.pack(pady=10)

        # Create the button to run Nobilis upload
        self.run_button_nobilis = tk.Button(self.root, text="Subir Pacientes", command=self.post_nobilis, width="30")
        self.run_button_nobilis.pack(pady=5) 

        # Create the button to run Nobilis errors
        self.run_button_nobilis_errors = tk.Button(self.root, text="Ver Errores", command=self.see_errors, width="30")
        self.run_button_nobilis_errors.pack(pady=5) 

        # Create the button to run Nobilis correct errors
        self.run_button_nobilis_correct = tk.Button(self.root, text="Subir Corregidos", command=self.post_errors, width="30")
        self.run_button_nobilis_correct.pack(pady=5) 

        # Create the status bar
        self.status = tk.Label(self.root, text="Preparado para cargar archivo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.geometry("400x700")
        self.root.mainloop()

    def open_sample_file(self):
        filepath = "./help/example_file.xlsx"
        full_path = os.path.abspath(filepath)
        try:
            os.startfile(full_path)
        except Exception as e:
            messagebox.showerror("Error", e)

    def proceedure(self):
        from tkinter import messagebox

        # list of items
        items = [
            "Abrir archivo excel con el botón Seleccionar archivo", 
            "Verificar que sea un formato válido", 
            "Una vez verificado el archivo, click en el botón Subir a MSP"
            ]

        # create a message with newlines for each item
        message = "El procedimiento es:\n"
        for item in items:
            message += "- " + item + "\n"

        # display the message box
        messagebox.showinfo("Order", message)

    def open_file_msp(self):
        # Clear the table
        self.table.delete(0, tk.END)
        headers_needed = [
            "Tipo de documento",
            "País",
            "Documento",
            "Nombre",
            "Fecha de nacimiento",
            "Departamento",
            "Celular",
            "Estudio",
            "Fecha toma muestra",
            "Fecha informe",
            "Resultado",
            "Procedencia"]
        headers_infile = []
        # Open a file dialog to select the Excel file
        self.filepath = filedialog.askopenfilename()
        # Read the first three rows of the Excel file
        try:
            df = pd.read_excel(self.filepath)
            headers = df.columns
            # Crear array con los encabezados del excel brindado por el usuario
            # que son iguales que los encabezados requeridos
            for header in headers:
                if header in headers_needed:
                    headers_infile.append(header)
                    print(f"Load header: {header}")
            # Si hay la misma cantidad de encabezados iguales en ambos arrays
            # esta OK
            if len(headers_needed) == len(headers_infile):
                counter = 0
                for header in headers_needed:
                    counter += 1
                    self.table.insert(tk.END, f"{counter} - {header}")
                self.status_label.config(text="Archivo Correcto", fg='green') 
                self.status.config(text="OK")
                self.status_ok = True  
                print("File loaded OK")
                # Leer archivo y cargar datos en DB
                self.cargar_datos_db('MSP')
            # de lo contrario muestra en pantalla los encabezados que estarian faltando
            else: 
                difference = set(headers_needed) - set(headers_infile)
                for header in difference:
                    self.table.insert(tk.END, f"Falta columna: {header}")
                    print(f"Header missing: {header}")
                self.status_label.config(text="Faltan columnas en archivo", fg='red')
                self.status.config(text="Error")
        except:
            self.status_label.config(text="Archivo inválido", fg='red')
            self.status.config(text="Error")

    def open_file_nobilis(self): # DEV to nobilis
        # Clear the table
        self.table.delete(0, tk.END)
        headers_needed = [
            "Institución",
            "1er Nombre",
            "1er Apellido",
            "Tipo de documento",
            "nº documento",
            "Fecha de nacimiento",
            "TELEFONOS",
            "Derivado a:",
            "Fecha de toma de muestra",
            "Procedencia",
            "Locación",
            "Dirección",
            "Correo para enviar resultado",
            "Examen",
            "Servicio",
            ]
        headers_infile = []
        # Open a file dialog to select the Excel file
        self.filepath = filedialog.askopenfilename()
        # Read the first three rows of the Excel file
        try:
            df = pd.read_excel(self.filepath)
            headers = df.columns
            # Crear array con los encabezados del excel brindado por el usuario
            # que son iguales que los encabezados requeridos
            for header in headers:
                if header in headers_needed:
                    headers_infile.append(header)
                    print(f"Load header: {header}")
            # Si hay la misma cantidad de encabezados iguales en ambos arrays
            # esta OK
            if len(headers_needed) == len(headers_infile):
                counter = 0
                for header in headers_needed:
                    counter += 1
                    self.table.insert(tk.END, f"{counter} - {header}")
                self.status_label.config(text="Archivo Correcto", fg='green') 
                self.status.config(text="OK")
                self.status_ok = True  
                print("File loaded OK")
                # Leer archivo y cargar datos en DB
                self.cargar_datos_db('nobilis')
            # de lo contrario muestra en pantalla los encabezados que estarian faltando
            else: 
                difference = set(headers_needed) - set(headers_infile)
                for header in difference:
                    self.table.insert(tk.END, f"Falta columna: {header}")
                    print(f"Header missing: {header}")
                self.status_label.config(text="Faltan columnas en archivo", fg='red')
                self.status.config(text="Error")
        except Exception as e:
            self.status_label.config(text="Archivo inválido", fg='red')
            self.status.config(text="Error")
            print("Error insertando archivo en db:\n", e)

    def cargar_datos_db(self, platform):
        if self.status_ok:
            if platform == 'MSP':
                # Run Selenium to send the data from the Excel file to the website form
                print("Reading file and inserting data in db...")
                ReadFile(self.filepath, 'MSP')
            else:
                # Run Selenium to send the data from the Excel file to the website form
                print("Reading file and inserting data in db...")
                ReadFile(self.filepath, 'NOBILIS')

    def run_selenium(self):
        if self.status_ok:
            try:
                # Run Selenium to send the data from the Excel file to the website form
                print("Run Selenium")
                file_id = get_last_file_id_msp()
                data = get_pendings_by_file_msp(file_id)
                payload = self.handle_payloads(data)
                ManageBrowser(payload=payload).insertar_datos()
            except Exception as e:
                response = messagebox.askyesno(
                        title="Error en archivo", 
                        message="Archivo Excel ya ingresado, si desea ingresar datos previos, click en Si."
                        )
                if response:
                    # Run Selenium to send the data from the Excel file to the website form
                    print("Run Selenium")
                    file_id = get_last_file_id_msp()
                    data = get_pendings_by_file_msp(file_id)
                    # create the payload
                    payload = self.handle_payloads(data, 'MSP')
                    ManageBrowser(payload=payload).insertar_datos()
                else:
                    self.table.delete(0, tk.END)

        else:
            messagebox.showerror("Error", "Es necesario ingresar un archivo Excel con formato válido primero.")

    def upload_pendings(self):
        try:
            data = get_pendings_msp()
            # create the payload
            payload = self.handle_payloads(data, 'MSP')
            ManageBrowser(payload=payload).insertar_datos()
        except Exception as e:
            messagebox.showerror("Error", "No se han encontrado pendientes, carga un nuevo archivo Excel primero.")
            print(e)

    def post_nobilis(self):
        try:
            data = get_pendings_nobilis()
            # create the payload
            payload = self.handle_payloads(data, 'NOBILIS')
            print(f"PAYLOAD:\n\n{payload}")
            CargaNobilis(payload)
        except Exception as e:
            messagebox.showerror("Error", "No se han encontrado pendientes, carga un nuevo archivo Excel primero.")
            print(e)

    def see_errors(self):
        try:
            errors = get_errors_nobilis()
            # open the file in write mode
            if errors != []:
                with open("errors.txt", "w") as file:
                    # write some text to the file
                    for error in errors:
                        line = "|".join(str(x) for x in error)
                        file.write(line + "\n\n")
                folder_path = "errors.txt"
                os.startfile(folder_path)
                print("see errors")
            else:
                messagebox.showinfo("Limpio", "No hay errores para corregir.")
        except Exception as e:
            print(e)

    def post_errors(self): # DEV to nobilis
        print("post errors")
        
    def handle_payloads(self, data, platform): # DEV to nobilis
        # create the payload
        payload = []
        if platform == 'MSP':
            for row in data:
                data = {
                    "Tipo de documento" : row[1],
                    "Pais" : row[2],
                    "Documento" : row[3], 
                    "Nombre" : row[4],
                    "Fecha de nacimiento" : row[5],
                    "Departamento" : row[6],
                    "Celular" : row[7],
                    "Motivo" : row[8],
                    "Tiene sintomas" : row[9],
                    "Fecha inicio sintomas" : row[10],
                    "Test" : row[11],
                    "Fecha toma de muestra" : row[12],
                    "Fecha informe" : row[13],
                    "Resultado" : row[14],
                    "Procedencia" : row[15],
                    "Realizado en" : row[16],
                    "Fecha creacion" : row[17],
                    "Subido" : row[18],
                    "Fecha subido" : row[19],
                    "file_id" : row[20]
                    }
                payload.append(data)
        else:
            for row in data:
                data = {
                    "idTipoDocumento" : row[1],
                    "nroDoc" : row[2],
                    "fechaNacimiento" : row[3], 
                    "domicilio" : row[4],
                    "telefono" : row[5],
                    "fechaAlta" : row[6],
                    "localidadOrigenDesc" : row[7],
                    "sexo" : row[8],
                    "nroHistoriaClinica" : row[9],
                    "email" : row[10],
                    "nombre" : row[11],
                    "apellido" : row[12],
                    "habilitado" : row[13],
                    "institucionesDesc" : row[14],
                    "planDesc" : row[15],
                    # ORDEN
                    'centroDesc': row[16],
                    'origenPacienteDesc': row[17],
                    'servicioDesc': row[18],
                    'locacionDesc':row[19],
                    'urgente': row[20],
                    'autorizada': row[21],
                    'ordenPendiente': row[22],
                    'prescripcionMedica':row[23],
                    "estudios" : row[24],
                    'nroHistClinica': row[9],
                    # both
                    "file_id" : row[25],
                    "created" : row[27]
                    }
                payload.append(data)
        return payload
    
    
    def clean(self):
        file_path = "database/database.db"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} was deleted successfully")
            Base.metadata.create_all(engine)
            print("Database created again succesfully!")
        else:
            print(f"{file_path} does not exist")