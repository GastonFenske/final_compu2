FROM python:3.8-buster

WORKDIR /app

COPY . /app

EXPOSE 1234

RUN cd /app/api/iqoptionapi && \
    python3 setup.py install

RUN pip install -r requirements.txt

CMD ["python", "-u", "./app.py"]
