FROM ubuntu:16.04
MAINTAINER Dieter De Witte drdwitte@gmail.com
RUN apt-get update 
RUN apt-get install -y nano wget unzip default-jdk maven
RUN mkdir /home/dockeruser
WORKDIR /home/dockeruser
RUN wget https://github.com/rdfhdt/hdt-java/archive/master.zip
RUN unzip master.zip
WORKDIR /home/dockeruser/hdt-java-master
RUN mvn install
WORKDIR /home/dockeruser/hdt-java-master/hdt-fuseki
RUN mvn package dependency:copy-dependencies
RUN mkdir /data
RUN wget https://raw.githubusercontent.com/drdwitte/rdfbenchmarking/master/setup/endpoints/FusekiHDT/fuseki_watdiv.ttl
RUN wget https://raw.githubusercontent.com/drdwitte/rdfbenchmarking/master/setup/endpoints/FusekiHDT/bin/hdtEndpoint.sh
RUN chmod 777 hdtEndpoint.sh
RUN mv hdtEndpoint.sh ./bin/hdtEndpoint.sh
CMD /bin/bash


