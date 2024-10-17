FROM python:3 
WORKDIR /clima
COPY requirements.txt ./
COPY clima.py .
CMD [ "python","./clima.py" ]