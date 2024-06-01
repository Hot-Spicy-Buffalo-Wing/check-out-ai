FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry

ENV PATH="/etc/poetry/bin:$PATH"

WORKDIR /check-out-ai
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./src ./src
WORKDIR /check-out-ai/src

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]