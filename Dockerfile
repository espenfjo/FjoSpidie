FROM debian:jessie
MAINTAINER espen@mrfjo.org
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
VOLUME /mnt/fjospidie
RUN echo "deb http://packages.linuxmint.com debian import" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install --no-install-recommends --force-yes -y -q git python python-setuptools libyaml-dev libpq-dev python-dev libpcap-dev net-tools openjdk-7-jre firefox xvfb graphviz python-yara ca-certificates python-pymongo python-dnspython python-yaml python-pydot python-configobj python-simplejson build-essential python-pymongo-ext python-gridfs && \
    cd /opt && git clone https://github.com/espenfjo/FjoSpidie.git

WORKDIR /opt/FjoSpidie

RUN python ez_setup.py install && \
    cp fjospidie.conf.dist fjospidie.conf

ENTRYPOINT ["./entrypoint.sh"]
