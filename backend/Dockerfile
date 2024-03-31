FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements ./requirements
COPY ./data_classes.py ./data_classes.py
COPY dbdupe.py ./db.py
COPY ./main.py ./main.py
COPY ./eveapicommunication.py ./eveapicommunication.py

RUN pip install -r ./requirements

RUN useradd -m --create-home appuser
USER appuser

CMD ["python3.11", "./main.py"]

EXPOSE 5000
