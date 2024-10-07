FROM python:3.11

RUN apt-get -y update
RUN apt-get install --assume-yes vim htop

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
COPY entrypoint.sh /app/
COPY alembic.ini /app/
COPY alembic /app/alembic
COPY core /app/core
COPY tests /app/tests

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:/usr/local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false
RUN poetry self update
RUN poetry install --only main --no-interaction --no-ansi

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8010"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8010/health/ || exit 1

EXPOSE 8010
