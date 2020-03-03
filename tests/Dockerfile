FROM python:alpine3.7

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache python3 bash jpeg-dev zlib-dev libjpeg g++ libxslt-dev && \
    pip3 install selenium pytest pytest-html eyes-selenium
