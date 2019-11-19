FROM python:3.8-alpine

COPY docker-entrypoint.sh /

# Setup date and runtime user encapsulation
RUN apk add --no-cache tzdata tini su-exec \
 && cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
 && addgroup -g 1000 -S python \
 && adduser -u 1000 -S python -G python \
 # Upgrade pip to avoid warning
 && pip install --upgrade pip \
 # Setup entrypoint
 && chmod +x /docker-entrypoint.sh

WORKDIR /home/python/app

COPY requirements.txt .

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev libffi-dev make \
 && pip install -r requirements.txt \
 && apk del build-dependencies

COPY --chown=python:python . .

ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

