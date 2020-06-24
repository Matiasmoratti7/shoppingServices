FROM python:3.8.2

WORKDIR /user_auth_rs

COPY . .

RUN pip install -r docker/dependencies

ENV FLASK_APP user_auth_rs
ENV FLASK_ENV development

EXPOSE 3000

CMD python serve.py