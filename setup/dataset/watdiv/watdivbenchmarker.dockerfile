FROM ubuntu:14.04
MAINTAINER Dieter De Witte <drdwitt@gmail.com>

#avoid dialogs during installation process:
ENV DEBIAN_FRONTEND noninteractive

RUN sudo apt-get update

#need make and gcc
RUN sudo apt-get install -y build-essential

#specific dependensies for watdiv: boost and dictionary in /usr/share/dict
RUN sudo apt-get install -y wget libboost-all-dev 
RUN sudo apt-get install -y dictionaries-common
ENV BOOST_HOME "/usr/share/boostbuild"

#download watdiv
RUN mkdir /tmp/download/
WORKDIR /tmp/download/
RUN wget http://dsg.uwaterloo.ca/watdiv/watdiv_v05.tar
RUN tar xvf watdiv_v05.tar
#install  

RUN mv /tmp/download/watdiv /usr/local/watdiv
RUN rm watdiv_v05.tar
WORKDIR /usr/local/watdiv

RUN sudo apt-get install -y miscfiles
RUN make
RUN wget -O- -q http://s3tools.org/repo/deb-all/stable/s3tools.key | sudo apt-key add -
RUN sudo wget -O/etc/apt/sources.list.d/s3tools.list http://s3tools.org/repo/deb-all/stable/s3tools.list
RUN sudo apt-get update && sudo apt-get install -y s3cmd
