FROM bitnami/python:3.9

WORKDIR /WIB

COPY requirements.txt /WIB/requirements.txt

ENV PYTHONUNBUFFERED 1

COPY ./app /WIB/app

COPY ./.env /WIB/.env

COPY main.py /WIB/main.py

CMD ["uvicon", "app:app:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]

RUN pip install --no-cache-dir --upgrade -r /WIB/requirements.txt

RUN pip install --upgrade pip