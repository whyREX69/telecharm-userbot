FROM python:3.10.2-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export --output requirements.txt --without-hashes --extras fast

FROM python:3.10.2-slim

WORKDIR /userbot

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /userbot/requirements.txt

COPY . .

CMD ["python", "-m", "app"]