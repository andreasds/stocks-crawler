ARG PYTHON=3.9.1-slim-buster

FROM python:${PYTHON}

RUN apt update \
  && apt install -y nano git \
  && mkdir -p /home/stocks/crawler

WORKDIR /home/stocks/crawler

ENTRYPOINT bash
