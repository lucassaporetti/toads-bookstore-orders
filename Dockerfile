FROM acidrain/python-poetry:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo

WORKDIR /app

RUN apt-get update -y && \
    apt-get install make curl -y && \
    apt-get clean -y && \
    pip install --upgrade pip

COPY pyproject.toml ./

RUN poetry config installer.parallel true
RUN poetry config virtualenvs.create false
RUN poetry update self
RUN poetry install

COPY alembic.ini/ ./
COPY app/ ./app/

EXPOSE 8000
CMD ["python", "-m", "app"]