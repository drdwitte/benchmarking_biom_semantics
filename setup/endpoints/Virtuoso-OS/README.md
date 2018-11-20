
### Setup Virtuoso OS Docker 

* Install docker container requires a single command: 
    - `sudo docker run --name virtuoso -p 8890:8890 -p 1111:1111 -e DBA_PASSWORD=dba -e SPARQL_UPDATE=true -e DEFAULT_GRAPH=http://www.example.com/my-graph -v /users/drdwitte/data:/data -d tenforce/virtuoso`
    - details: 
        - `-v /home/ddewitte/data:/data` shared directory between linux VM and docker container 
        - `-d` run container as a daemon
        - `-p 8890:8890 -p 1111:1111` Virtuoso uses these ports   
        - `-e` extra parameters for docker container, more info on docker hub: https://hub.docker.com/r/tenforce/virtuoso/

* `docker start|stop` at the same time start virtuoso, so stopping virtuoso inside the container will automatically stop the container. 

* add a shell as follows: `sudo docker exec -it virtuoso /bin/bash`

* The shared folder /data contains all the extra data: the database file, the configuration file,... this means that even after breaking the container Virtuoso could be restored since everything is in the shared folder.

* ISSUE in container: errors related to terminal can be solved by: `export TERM=xterm`, you have to run this every time you connect to the container


### Virtuoso Configuration: Virtuoso.ini

* We use an .ini file which was offered to use by OpenLink after sending out an RFI

* additional (not in docker => read-only filesystem): <a href="http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/VirtRDFPerformanceTuning#Linux-only%20--%20%E2%80%9Dswappiness%22"> Performance Tuning Swappiness</a> 
	- `sudo /sbin/sysctl -w vm.swappiness=10`

### Load Data in via Bulk Loader

- From /usr/local/virtuoso-opensource run the following

- `sudo bin/isql-v 1111 dba dba exec="ld_dir('/data/', '*.nt.gz', 'http://watdiv.com/');"`
- `sudo bin/isql-v 1111 dba dba exec="rdf_loader_run();" &`

- Checking for status: 
	- Shows the progress of the bulk loader: `sudo bin/isql-v 1111 dba dba exec="select * from DB.DBA.load_list;"`
	- Count the amount of triples currently present in the default graph: `sudo bin/isql-v 1111 dba dba exec="sparql select count(*) where {?s ?p ?o};"`
