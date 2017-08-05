FROM python:3.6
ENV PYTHONBUFFERED 1
ARG server_port
EXPOSE $server_port

COPY ./requirements.txt /vat/tmp/requirements.txt
RUN pip install -r /vat/tmp/requirements.txt

RUN mkdir /srv/app
WORKDIR /srv/app

CMD main.py --port=$server_port
