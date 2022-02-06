# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

###############################################
# Base Image
###############################################
FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    CHROMEDRIVER_DIR="/chromedriver"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install Chrome
RUN apt-get -y update \
    && apt-get install --no-install-recommends -y \
    wget \
    unzip \
    joe \
    gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable

###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d $CHROMEDRIVER_DIR


# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.8
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
COPY ./.env ./.secrets.toml ./settings.toml ./

# Copying in our entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

# Install only dependencies: - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

###############################################
# Production Image
###############################################
FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base $CHROMEDRIVER_DIR $CHROMEDRIVER_DIR
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
