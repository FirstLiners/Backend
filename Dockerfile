FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app

# copy .env file to /app

COPY .env /app

RUN  pip3 install -r /app/requirements.txt --no-cache-


COPY ./src /app


RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
