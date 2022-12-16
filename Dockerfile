FROM python:3.10-bullseye as builder

WORKDIR /opt/app

COPY requirements.txt /opt/app
RUN pip install -r requirements.txt

FROM python:3.10-slim-bullseye as runner

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

ARG UID
ARG GID
ARG USERNAME
ARG GROUPNAME

RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/

RUN mkdir -p /home/$USERNAME/morierus
RUN mkdir -p /home/$USERNAME/share

COPY morieru-dl.py /home/$USERNAME/
COPY requirements.lock /home/$USERNAME/
COPY .env /home/$USERNAME/
COPY robust-zenith-286413-64cf0e236cad.json /home/$USERNAME/

RUN pip install -r requirements.lock

CMD ["python","morieru-dl.py"]
