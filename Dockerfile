FROM python:3.9.6 AS configurator

WORKDIR /

COPY main.py .

RUN pip3 freeze > requirements.txt

FROM python:3.9.6 AS builder

RUN pip3 install pyinstaller

WORKDIR /app

COPY --from=configurator /requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .

RUN pyinstaller -y -n yamlpatch main.py

FROM alpine:3.14

COPY --chown=0:0 --from=builder /app/dist /usr/local/bin

RUN chmod +x /usr/local/bin/yamlpatch