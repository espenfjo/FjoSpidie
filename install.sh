mvn install:install-file -Dfile=lib/jnetpcap.jar -DgroupId=jnetpcap -DartifactId=jnetpcap -Dversion=1.3  -Dpackaging=jar
mvn install:install-file -Dfile=lib/jnetpcap-native-linux.jar -DgroupId=jnetpcap -DartifactId=jnetpcap-native -Dversion=1.3 -Dclassifier=linux -Dpackaging=jar
mvn install:install-file -Dfile=lib/browsermob-proxy-2.0-beta-8.jar -DgroupId=org.browsermob -DartifactId=browsermob-proxy -Dversion=2.0-beta-8 -Dpackaging=jar
mvn install:install-file -Dfile=lib/harlib-1.1.1.jar -DgroupId=benchlab -DartifactId=harlib -Dversion=1.1.1 -Dpackaging=jar