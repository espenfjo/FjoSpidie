FROM tianon/debian:wheezy

ENV DEBIAN_FRONTEND noninteractive
RUN echo "deb http://packages.linuxmint.com debian import" >> /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get install --force-yes -y -q python python-setuptools libyaml-dev libpq-dev python-dev libpcap-dev git net-tools openjdk-7-jre firefox xvfb graphviz snort


RUN git clone https://github.com/espenfjo/FjoSpidie.git --single-branch -b v2 /opt/fjospidie
RUN python /opt/fjospidie/ez_setup.py install
ENV RUNNABLE_USER_DIR /opt/fjospidie