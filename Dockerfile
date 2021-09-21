FROM python:3.9.7-alpine3.14 AS builder

RUN apk --update --no-cache add \
    zlib-dev \
    musl-dev \
    libc-dev \
    gcc \
    git \
    pwgen

RUN pip3 install pyinstaller

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .

RUN pyinstaller -F -y -n yamlpatch main.py

FROM alpine:3.14

COPY --chown=0:0 --from=builder /app/dist /usr/local/bin

RUN chmod +x /usr/local/bin/yamlpatch

CMD ["sh"]