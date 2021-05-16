FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install --no-install-recommends -yq \
      gcc \
      g++ \
      libc-dev \
      libpq-dev \
      gdal-bin \
      libgdal-dev \
      make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install requirements into a separate layer
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy the code
COPY . /app
