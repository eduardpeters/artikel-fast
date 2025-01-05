FROM python:3.12-alpine

WORKDIR /seed_data

COPY ./seed_data/nouns.json /seed_data/nouns.json

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]