FROM python:3.8.2

WORKDIR /storage_rs

COPY . .

RUN pip install -r docker/dependencies

ENV FLASK_APP storage_rs
ENV FLASK_ENV development

EXPOSE 27017 4000

CMD python serve.py