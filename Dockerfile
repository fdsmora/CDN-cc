FROM ubuntu:latest
MAINTAINER Fausto Mora "fausto.ds.mora@gmail.com"
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    curl
ENV FLASK_APP=app
ENV FLASK_ENV=development
COPY . /CDN-cc
WORKDIR /CDN-cc
RUN pip3 install -r /CDN-cc/requirements.txt
EXPOSE 5000
ENTRYPOINT [ "/CDN-cc/run_this_app.sh" ]
