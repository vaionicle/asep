FROM python:3.11

WORKDIR /opt/asep

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt