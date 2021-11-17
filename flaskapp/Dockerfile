FROM python:alpine

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /root
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

WORKDIR /var/www/flaskapp

USER www

EXPOSE 5000

CMD ["./entrypoint.sh"]