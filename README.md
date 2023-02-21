# Carga automática para MSP y Nobilis

## Instalación en Windows:
  1. Asegurarse de tener Python instalado, de lo contrario hay un instalador en la carpeta "install" en el root del repositorio
  2. Correr archivo "instalar.bat"
  3. Correr "ejecutar.bat" para iniciar

## Instalación en Linux:
  1. instalar virtualenv 
  2. virtualenv ./env
  3. source ./env/bin/activate
  4. (env) pip3 install -r ./requirements.txt
  5. inciar con python3 main.py

## Para MSP:
  ## variables.py:
    - Completar variables con usuario y contraseña
    - Completar la url
    
## Para Nobilis:
  ## upload_to_nobilis.py:
    - completar las variables wsdl_url con sus respectivas url
    - elegir que datos se suben en los objetos paciente y orden.
