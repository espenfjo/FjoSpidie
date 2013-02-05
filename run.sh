#!/bin/bash
xvfb-run -a java -Djava.library.path=target/lib/ -jar target/com.efo.fjospidie-1.0-SNAPSHOT-jar-with-dependencies.jar $@