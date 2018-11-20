#!bin/bash

sudo bin/isql 12202 dba dba exec="rdf_loader_run();" &
sudo bin/isql 12202 dba dba exec="rdf_loader_run();" &
sudo bin/isql 12202 dba dba exec="rdf_loader_run();" &
wait
sudo bin/isql 12202 dba dba exec="checkpoint;" 
echo 'Done checkpointing'
