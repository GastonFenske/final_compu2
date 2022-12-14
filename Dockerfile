FROM python:3.9-alpine

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

# RUN apk update
# RUN apk add make automake gcc g++ subversion python3-dev
RUN apk add --update curl gcc g++ libffi-dev openssl-dev build-base linux-headers && \
    apk add mariadb-dev py3-mysqlclient mysql-client && \
    rm -rf /var/cache/apk/*

# COPY requirements.txt /home/app
# ADD requirements.txt ./requirements.txt
# RUN bash iqapi.sh
RUN cd /home/app/api/iqoptionapi && \
    python3 setup.py install

ADD requirements.txt ./requirements.txt

RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1234

CMD ["python", "./app.py"]
