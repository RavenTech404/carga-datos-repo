@ECHO OFF

cmd /k "pip install virtualenv && virtualenv env && env\Scripts\activate.bat && pip install -r .\requirements.txt && exit"

PAUSE