FROM bitnami/python:3.9

RUN pip install --upgrade pip

WORKDIR /WIB

COPY requirements.txt /WIB/requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade -r /WIB/requirements.txt

COPY ./app /WIB/app

COPY ./.env /WIB/.env

COPY main.py /WIB/main.py

CMD ["uvicon", "app:app:app", "--host", "127.0.0.1", "--port", "8000"]