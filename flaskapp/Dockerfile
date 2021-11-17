FROM ubuntu:latest

ENV GROUP_ID=1000 \
    USER_ID=1000

RUN apt update && apt install -y \
    build-essential libssl-dev libffi-dev python3-dev python3-pip mongodb-clients

WORKDIR /root
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --system --uid $USER_ID --gid $GROUP_ID --shell /bin/bash www

WORKDIR /var/www/flaskapp

USER www

EXPOSE 5000

CMD ["./entrypoint.sh"]