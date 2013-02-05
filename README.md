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

Build
=====
Run `mvn package`


Usage
=====
Run run.sh --url http://www.google.com to analyse google.com.