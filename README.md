FjoSpidie
=========

FjoSpidie Honey Client

This Honey Client will launch Firefox against a given URL and create a HAR of the URL.

This HAR is used to create a PNG over all the domains visited.
A tcpdump will also be recored of the session. The tcpdump will be run through snort to search for known threats or issues.
Any autodownloaded file will be stored in the database for later review.

Requirements
============
* xfvb
* maven
* mysql

Build
=====
Run `mvn package`


Configuration
=============
Configure `fjospidie.conf` from the `fjospidie.conf.sample` file.

Usage
=====
Run `run.sh --url http://www.google.com` to analyse google.com.




See https://www.dropbox.com/s/eiwul3ipmqto57s/Screenshot%202013-10-26%2021.35.40.png for a picture of how it may look
with the default web frontend looks.
