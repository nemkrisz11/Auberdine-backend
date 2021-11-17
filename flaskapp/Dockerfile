FROM ubuntu:latest

ENV GROUP_ID=1000 \
    USER_ID=1000

# install the mongo client
RUN apt update
RUN apt install -y mongodb-clients python3 pip

WORKDIR /root
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --system --uid $USER_ID --gid $GROUP_ID --shell /bin/sh www

WORKDIR /var/www/flaskapp

USER www

EXPOSE 5000

CMD ["./entrypoint.sh"]