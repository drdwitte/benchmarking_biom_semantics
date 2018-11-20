#!bin/bash

#clean up files of previous test
rm ./unit_test/*.csv
rm ./unit_test/*.log
rm -r cmd/target
mvn package -Dmaven.test.skip=true

./cmd/benchmark -m ./unit_test/listfiles.txt -r 10 -o 1 -w 1 -q http://sparql.org/books/sparql -p 8 -c ./unit_test/results.csv -t 10 --log-file unit_test/runner.log --store-results-dir unit_test/SparqlResults > unit_test/output.log
