FROM debian:12

RUN apt-get update \
 && apt-get install --yes python3-full python3-poetry \
 && apt-get install --yes postgresql-client libpq-dev \
 && apt-get install --yes libnss3 libnspr4 libdrm2 libgbm1 libasound2

RUN adduser --disabled-password --home '/app' app
WORKDIR /app
USER app

COPY pyproject.toml poetry.lock README.md  ./
RUN poetry install && poetry run playwright install
COPY .  ./

# RUN apk add --update --no-cache --virtual .build-deps build-base postgresql-dev python3-dev \
#  && poetry install \
#  && apk del --no-network .build-deps


# ENTRYPOINT ["poetry", "run", "--"]
