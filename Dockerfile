FROM python:3.8-alpine3.15

WORKDIR /app

COPY . /app

EXPOSE 1234

RUN apk add --update curl gcc g++ libffi-dev openssl-dev build-base linux-headers && \
    apk add mariadb-dev py3-mysqlclient mysql-client && \
    rm -rf /var/cache/apk/*

RUN cd /app/api/iqoptionapi && \
    python3 setup.py install

RUN pip install -r requirements.txt

CMD ["python", "./app.py"]
