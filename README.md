FjoSpidie v2
=========

FjoSpidie Honey Client

This time the spider is written in Python instead of Java.

This version isnt done yet, but it is in development, and the code is lighter, and it has lighter requirements.

This Honey Client will launch Firefox against a given URL and create a HAR of the URL.

This HAR is used to create a PNG over all the domains visited.
A tcpdump will also be recored of the session. The tcpdump will be run through snort to search for known threats or issues.
Any autodownloaded file will be stored in the database for later review.


Requirements
============
* xfvb
* python
* postgresql
* python-setuptools
* yaml

Build
=====
python ez_setup.py install


Configuration
=============
Configure `fjospidie.conf` from the `fjospidie.conf.dist` file.

Usage
=====
Run `python fjospidie --url http://www.google.com` to analyse google.com.
or run `xvfb-run -a python fjospidie --url http://www.google.com` to run the spider in a xvfb server isntead
of the default X11 server.

Web Interface
=============
The FjoSpidie Web interface can be found here:
https://github.com/espenfjo/fjospidie-interface



See https://www.dropbox.com/s/eiwul3ipmqto57s/Screenshot%202013-10-26%2021.35.40.png for a picture of how it may look
with the default web frontend looks.
