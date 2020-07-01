from ubuntu:20.04
RUN apt-get update &&  TZ="Europe/Paris" DEBIAN_FRONTEND="noninteractive" apt-get install apache2 python3 libexpat1 apache2-utils ssl-cert libapache2-mod-wsgi python3-pip libmysqlclient-dev --yes
RUN apt-get install --yes libpq-dev
COPY ./requirements.txt /tmp
RUN cat /tmp/requirements.txt |xargs -I {} pip3 install {}
COPY ./apache/conso-api.conf /etc/apache2/sites-available
RUN a2ensite conso-api.conf
COPY app /opt/conso-api
EXPOSE 80
CMD apachectl -D FOREGROUND
