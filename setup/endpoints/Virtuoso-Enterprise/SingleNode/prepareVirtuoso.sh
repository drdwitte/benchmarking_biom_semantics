#!/bin/bash

#prereq: sudo yum install nano

sudo mkfs -t ext4 /dev/xvdb
sudo /opt/virtuoso/bin/virtuoso-stop.sh
echo 'backup virtuoso dirs'
sudo mv /opt/virtuoso /opt/virtuoso_temp

sudo mkdir /opt/virtuoso
echo 'mounting xvdb'
sudo mount /dev/xvdb /opt/virtuoso
sudo chown ec2-user /opt/virtuoso
echo 'putting back original virtuoso dirs'
sudo mv /opt/virtuoso_temp/* /opt/virtuoso

cd /opt/virtuoso
sudo mkdir data
cd data

#optimization parameter recommended by OpenLink
sudo /sbin/sysctl -w vm.swappiness=10

#next: download RDF dataset in ./data folder

#check if disk is mounted on /opt/virtuoso:
lsblk
