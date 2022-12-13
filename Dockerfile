FROM python:3.8-alpine3.15

RUN mkdir -p /home/app

WORKDIR /home/app

COPY . /home/app


# RUN apk update
# RUN apk add make automake gcc g++ subversion python3-dev
RUN apk add --update curl gcc g++ libffi-dev openssl-dev build-base linux-headers && \
    apk add mariadb-dev py3-mysqlclient mysql-client && \
    rm -rf /var/cache/apk/*

# COPY requirements.txt /home/app
# ADD requirements.txt ./requirements.txt
ADD requirements.txt ./requirements.txt

RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1234



CMD ["python3", "/home/app/app.py"]
