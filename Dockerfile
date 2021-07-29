FROM python:3.9.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/srv
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/logs
WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY thomann .
