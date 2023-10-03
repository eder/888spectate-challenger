FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

RUN  pip install --upgrade pip
RUN  pip install --no-cache-dir -r requirements.txt

WORKDIR /www
COPY ./ /www

EXPOSE 8000:8000


