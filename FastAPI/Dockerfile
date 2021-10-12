FROM debian:latest

WORKDIR /my_server/

COPY requirements.txt requirements.txt

RUN apt update && apt install python3-pip -y && pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["uvicorn", "FastAPI_projet_2:api", "--host", "0.0.0.0", "--port", "8000"]
