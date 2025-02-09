FROM python:3.12

WORKDIR /app

COPY ./app /app/app
COPY ./alembic.ini /app/alembic.ini
COPY ./db_models /app/db_models
COPY ./alembic /app/alembic
COPY ./app/requirements.txt /app/requirements.txt

ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["sh", "-c", "alembic upgrade head; uvicorn app.main:app --host 0.0.0.0 --port 8000"]
