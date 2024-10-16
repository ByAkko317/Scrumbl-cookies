FROM python:3 
WORKDIR C:\Users\Pablo\OneDrive\Escritorio\UTN\Materias\2024\ORG EMPRESARIAL 2024\Proyecto Integrador
COPY requirements.txt ./
COPY clima.py .
CMD [ "python","./clima.py" ]