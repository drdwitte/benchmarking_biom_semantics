#!/bin/bash
for i
do
  echo $i
  mkdir -p $i
  cp $i.sparql $i/$i.sparql
  cd $i
  split -l 1 $i.sparql
  rm $i.sparql
  ls -d $PWD/* > ../$i.list
  cd ..
done