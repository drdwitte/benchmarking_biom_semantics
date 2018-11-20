FROM ubuntu:16.04
MAINTAINER Dieter De Witte drdwitte@gmail.com
RUN apt-get update 
RUN apt-get install -y wget unzip nano default-jdk s3cmd python-pip maven
RUN mkdir /home/dockeruser
WORKDIR /home/dockeruser
RUN wget https://github.com/drdwitte/rdfbenchmarking/archive/master.zip
RUN unzip master.zip
WORKDIR /home/dockeruser/rdfbenchmarking-master/benchmarksoftware/sparql-query-bm/
#builds from source and runs a unit test against sparql.org endpoint
RUN bash buildAndTest.sh
RUN pip install SPARQLWrapper
RUN pip install wget
RUN pip install requests
RUN pip install pyyaml
WORKDIR /home/dockeruser
RUN ln -s /home/dockeruser/rdfbenchmarking-master/benchmarksoftware/sparql-query-bm/cmd/benchmark ./
RUN mv /home/dockeruser/rdfbenchmarking-master/benchmarksoftware/bm-runner/BenchmarkRunnerDocker.py ./
RUN mv /home/dockeruser/rdfbenchmarking-master/benchmarksoftware/bm-runner/general_config.yaml ./
CMD /bin/bash


