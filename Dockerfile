FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get -y update; apt-get -y install postgresql-client

COPY requirements.txt .

RUN  pip install --upgrade pip
RUN  pip install --no-cache-dir -r requirements.txt


WORKDIR /www
COPY ./ /www

RUN chmod 744 ./bin/start-server.sh
RUN chmod +x ./bin/wait-for-it.sh

EXPOSE 8000:8000


