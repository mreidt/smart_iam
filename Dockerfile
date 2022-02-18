FROM python:3.9-alpine

ARG MODE=production
ENV MODE=${MODE}

WORKDIR /code
COPY ./requirements /code/requirements/

COPY ./ /code/
RUN apk add --no-cache --upgrade --virtual .build-deps \
    gcc \
    linux-headers \
    mariadb-client \
    musl-dev \
    mariadb-connector-c-dev \
    libxml2-dev \
    libxslt-dev \
    && pip3.9 install -U pip setuptools \
    && if [ "$MODE" != "development" ]; \
      then \
         pip install --no-cache-dir -r requirements/production.txt; \
         pip uninstall -y pip; \
         chmod -R 644 *; \
         chmod -R a+rx scripts smart_iam apps; \
      else \
         pip install --no-cache-dir -r requirements/development.txt; \
      fi \
    && apk del --no-cache .build-deps \
    && apk add musl mariadb-connector-c

RUN apk add bash pcre mariadb-connector-c-dev libxml2 libxslt # Runtime SO dependencies
RUN adduser -D -u 1000 -G www-data uwsgi
EXPOSE 8010

USER uwsgi
CMD ["bash", "scripts/start_server.sh"]
