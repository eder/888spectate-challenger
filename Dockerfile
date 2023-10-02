FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie sua aplicação para o contêiner
COPY ./app /app

#expose default port of the docker to 8000
EXPOSE 8000:8000


