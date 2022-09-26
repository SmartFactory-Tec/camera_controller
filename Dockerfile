FROM python:3.9-bullseye

ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt update; apt install -y libgl1

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:${POETRY_HOME}/venv/bin"

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./

RUN ["poetry", "install"]
COPY src ./src

CMD ["poetry","run", "python", "./src/main.py"]

