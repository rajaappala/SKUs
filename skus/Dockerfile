FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;

RUN mkdir /code

ADD . /code
WORKDIR /code

RUN pip install -U pip setuptools
RUN pip install -r requirements.txt

EXPOSE 8000

# copy entrypoint.sh
COPY ./entrypoint.sh .

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]