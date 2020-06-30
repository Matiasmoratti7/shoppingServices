FROM python:3.8.2

WORKDIR /email_rs

COPY . .

RUN pip install -r docker/dependencies

ENV FLASK_APP email_rs
ENV FLASK_ENV development

EXPOSE 2000

CMD python service.py