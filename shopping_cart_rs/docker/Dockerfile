FROM python:3.8.2

WORKDIR /shopping_cart_rs

COPY . .

RUN pip install -r docker/dependencies

ENV FLASK_APP shopping_cart_rs
ENV FLASK_ENV development

EXPOSE 5000

CMD python serve.py