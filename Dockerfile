FROM ubuntu:16.04

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN apt-get -y install python-tk
RUN pip install --upgrade pip
RUN pip install google-cloud-firestore
RUN pip install requests
RUN pip install pystan
RUN pip install fbprophet