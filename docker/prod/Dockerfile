ARG PYTHON=3.9.1-slim-buster

FROM python:${PYTHON}

RUN apt update \
  && apt install -y git \
  && mkdir -p /home/stocks/

RUN git clone https://github.com/andreasds/stocks-crawler.git \
  /home/stocks/crawler

WORKDIR /home/stocks/crawler
