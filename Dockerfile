FROM python:buster

COPY ./ /app
WORKDIR /app

RUN pip install -U pip
RUN pip install -r requirements-dev.txt

ENTRYPOINT [ "gunicorn", "-b", ":5000", "app:app" ]