FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
  less \
  vim

RUN useradd -s /bin/bash -m uwsgi

COPY . /etc/vinnyexpres

WORKDIR /etc/vinnyexpres

RUN pip3 install .

CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--uid", "uwsgi", "uwsgi.ini"]
