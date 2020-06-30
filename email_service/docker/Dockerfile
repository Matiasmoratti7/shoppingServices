FROM python:3.8.2

WORKDIR /email_service

COPY . .

RUN pip install -r docker/dependencies

ENV PYTHONUNBUFFERED=1

CMD python service.py