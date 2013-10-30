#!/bin/bash
PATH=/opt/snort/bin:$PATH
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
xvfb-run -a java -Djava.library.path=target/lib/ -jar target/com.efo.fjospidie-1.0-SNAPSHOT-jar-with-dependencies.jar ${1+"$@"}
