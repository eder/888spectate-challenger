FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8000:8000


