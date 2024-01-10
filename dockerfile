# start dockerfile with linux kernel slim bullseye image and python 3.11.6
FROM python:3.11.6-slim-bullseye

# option linux : python
ENV PYTHONUNBUFFERED = 1

# update and install dependencies
RUN apt-get update && apt-get -y install gcc libpq-dev

# create folder belong to our project and set working directory
WORKDIR /app
#RUN pip install --upgrade pip

# copy requirements.txt to /app
COPY requirements.txt /app/requirements.txt

# install requirements.txt
RUN pip install -r /app/requirements.txt

# copy all project files to /app
COPY . /app/

    

