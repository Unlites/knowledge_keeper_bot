FROM python:3.10-buster

WORKDIR /auth

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "auth_server.py"]
