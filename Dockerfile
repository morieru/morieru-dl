FROM python:3.10-bullseye as builder

WORKDIR /opt/app

COPY requirements.txt /opt/app
RUN pip install -r requirements.txt

FROM python:3.10-slim-bullseye as runner

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY morieru-dl.py /root/
COPY requirements.lock /root/
COPY .env /root/
COPY robust-zenith-286413-64cf0e236cad.json /root/

RUN pip install -r requirements.lock

CMD ["python","morieru-dl.py"]

