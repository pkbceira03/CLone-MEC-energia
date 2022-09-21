FROM python:3.10.5

RUN apt-get update && \
    apt-get install -y libpq-dev


WORKDIR /mec-energia-api

COPY . /mec-energia-api

RUN pip install --no-cache-dir -r requirements.txt