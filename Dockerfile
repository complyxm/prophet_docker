FROM ubuntu:16.04

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-tk
RUN pip3 install --upgrade pip3
RUN pip3 install google-cloud-firestore
RUN pip3 install requests
RUN pip3 install pystan
RUN pip3 install fbprophet