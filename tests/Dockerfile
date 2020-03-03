FROM python:alpine3.7

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg g++ libxslt-dev bash \
    && pip install Pillow \
    && apk del build-deps

RUN apk update && \
    apk add bash && \
    pip install selenium pytest pytest-html webdriver-manager eyes-selenium
