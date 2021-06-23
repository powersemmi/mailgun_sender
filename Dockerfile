FROM python:3.9-alpine
RUN printenv
RUN mkdir /mailgun
WORKDIR /mailgun

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN \
   apk add libc-dev && \
   apk add alpine-sdk && \
   apk add postgresql-dev && \
   apk add python3-dev && \
   apk add libffi-dev && \
   apk add wkhtmltopdf
COPY ./req.txt .
RUN pip install -U pip wheel setuptools
RUN python3 -m pip install -r req.txt
COPY . /mailgun

