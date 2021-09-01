FROM python:3.7-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev mariadb-connector-c-dev libffi-dev
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install --upgrade pip
RUN pip install uwsgi mozilla-django-oidc django

WORKDIR /etc/app
#COPY ./requirements.txt ./
#RUN pip install -r requirements.txt

COPY ./ ./
RUN python3 manage.py migrate
RUN chmod 777 .
RUN chmod 777 db.sqlite3

CMD ["uwsgi", "--chdir=/etc/app/", "--module=portal.wsgi:application", "--master", "--pidfile=/tmp/project-master.pid", "--http=0.0.0.0:8080", "--processes=5", "--uid=1000", "--gid=2000", "--harakiri=20", "--max-requests=5000", "--vacuum", "--honour-stdin"]

