FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"
WORKDIR /app

# Install poetry
RUN set +x \
    && apt update \
    && apt upgrade -y \
    && apt install -y curl gcc build-essential \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -\
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml /app/
RUN poetry install

# Prepare entrypoint
ADD . /app/
RUN chmod +x scripts/* \
    && poetry install
ENTRYPOINT ["docker-entrypoint.sh"]
