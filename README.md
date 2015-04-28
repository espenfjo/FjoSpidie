FjoSpidie v2.2
=========

FjoSpidie Honey Client

This Honey Client will launch Firefox and open a given URL and create graphs and analyses based on what Firefox does.

These graphs and analyses include:
* PNG diagram of all connections made
* TCPdump of all traffic
* IDS findings via Suricata based on the tcpdump
* Easy overview of every header and request/response

Usage
=====
Everything is done through Docker to ease installation and usage.

Simply run `docker run espenfjo/fjospidie --url http://www.google.com` to analyse http://www.google.com.
Run `docker run espenfjo/fjospidie --help` to see a complete list of available options.

To run with suricata you need access to suricatas socket.
If run through docker you can eg. run:
`docker run -v /mnt/fjospidie:/mnt/fjospidie -i -t espenfjo/fjospidie:last --url http://www.google.com/"`
This will mount `/mnt/fjospidie` from the host inside your container. `/mnt/fjospidie` needs to contain your Suricata socket.

Web Interface
=============
The FjoSpidie Web interface can be found here:
https://github.com/espenfjo/fjospidie-interface

See http://i.imgur.com/z9Hh0SQ.png for a screenshot of how it may look with the default web frontend.
