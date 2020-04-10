FROM python:buster

COPY ./ /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements-dev.txt

ENTRYPOINT [ "gunicorn", "-b", ":8080", "main:app" ]