FROM python:3.10  

WORKDIR /code
RUN pip install --no-cache-dir poetry
COPY ./pyproject.toml ./poetry.lock /code
RUN poetry install --no-interaction --no-ansi

COPY ./ /code
RUN poetry install --no-interaction --no-ansi

CMD ["poetry", \
    "run", \
    "uvicorn", \
    "--log-level", "debug", \
    "--factory", "api.main:create_app", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--reload"]
