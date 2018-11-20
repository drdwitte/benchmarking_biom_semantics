#!bin/bash

#https://docs.docker.com/engine/installation/linux/ubuntulinux/

#prereqs
sudo apt-get -y update
sudo apt-get -y install apt-transport-https ca-certificates

#add the new GPG key
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

#Ubuntu Trusty: 
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list

#Ubuntu Xenial
#echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list


sudo apt-get -y update 
sudo apt-get -y install linux-image-extra-$(uname -r) linux-image-extra-virtual

#install docker

sudo apt-get -y update 
sudo apt-get -y install docker-engine
sudo service docker start

#test a hello-world container
sudo docker run hello-world
