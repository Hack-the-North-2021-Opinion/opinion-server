FROM python:3.8

COPY server ./server
COPY requirements.txt ./
COPY certs ./certs

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./server/manage.py", "runserver", "0.0.0.0:8080"]