# Howto: Run watdiv benchmark from a to z

## TODO: double check

## 0. 

We use query-count 20 for the Watdiv simulations!!!

## 1. Watdiv container

Setup docker instance with watdiv pre-installed:

* `sudo docker build -t drdwitte/watdivbenchmarker -f watdivbenchmarker.dockerfile .`
* `sudo docker run -it drdwitte/watdivbenchmarker /bin/bash`

## 2. Creating triples data

Create triples: 
* `./watdiv -d ./model/wsdbm-data-model.txt scale-factor`
* *scale-factor* 1 means 100K triples 
* This results is a filed called saved.txt which is required for generating the queries

## 3. Preparing for query template generation (s3)

To generate the templated queries: `./watdiv -q ./model/wsdbm-data-model.txt queryfile query-count recurrence-factor`
* **WARNING** saved.txt has to be in the same directory from where you execute the watdiv command!!
* *queryfile* is the query template file, for example ./testsuite/C1.txt
* *query-count* number of queries per template => 20
* *recurrence factor* -> number of times query is repeated = 1

## 4. Actual query generation + preparation for Sparql benchmarker

* `python createTemplatedQueryies.py &` 
* packaging `tar -zcvf templated<XX>M.tar.gz ./templated`


