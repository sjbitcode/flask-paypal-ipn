FROM python:3.6-alpine

LABEL maintainer sjbitcode@gmail.com

ENV PYTHONUNBUFFERED="TRUE" APP_PATH="/app" LOG_PATH="/logs"
RUN mkdir -p $APP_PATH
RUN mkdir -p $APP_PATH/$LOG_PATH
WORKDIR $APP_PATH

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . $APP_PATH

VOLUME [$APP_PATH]
