FROM ubuntu:20.04
LABEL maintainer="Jacob Sundqvist <jacob.sundqvist@ninc.io>"

# Create app directory
WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install -r requirements.txt