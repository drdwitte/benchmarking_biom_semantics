# Specifics for Virtuoso Cluster setup

* Same setup as Virtuoso Enterprise edition (single node) apart from VPC:
	- Configure VPC: open the following ports:
		* 12201, 12202, 12203 are the isql ports for node 1-3
		* 22201, 22202, 22203 are the internal communication ports for the cluster	

* Download the dataset in EVERY node, Virtuoso can decide for itself in which node a file is loaded

* Link to Cluster setup documentation Openlink: http://docs.openlinksw.com/virtuoso/clusterstcnfsetup/

* remove default database directories, cluster scripts will generate new ones

* create cluster config files on the master node:
	- `export CLUSTER_SIZE=3`
 	- `sudo /opt/virtuoso/bin/virtuoso-mkcluster.sh -cluster-size 3`

* move the clusterX directories to the other nodes and modify the cluster.ini files:
	- (add the [ELASTIC] part)
	- host1-3 should be the actual IP addresses (the mkcluster script creates a cluster on a single node!)

	<!--  sudo mkdir backup #in every node -->
	<!--  sudo ln -s /opt/virtuoso/bin/virtuoso-iodbc-t virtuoso	-->
	<!--  NOTE virtuoso.ini for master node is different! -->
	<!--  #master .ini heeft [HTTPServer], [Zero Config], [URIQA], [SPARQL], [Plugins]-->


* cluster.ini: (for the other nodes change ThisHost to Host2 and Host3 specifically)

-- BEGIN cluster.ini

[Cluster]

Threads             = 20

Master              = Host1

ThisHost            = Host1

ReqBatchSize        = 10000

BatchesPerRPC       = 4

BatchBufferBytes    = 20000

LocalOnly           = 2

MaxKeepAlivesMissed = 1000

Host1               = 172.31.53.17:22201

Host2               = 172.31.62.207:22202

Host3               = 172.31.61.253:22203

MaxHosts            = 4

[ELASTIC]

Segment1 = 4G, database.db = q1

Slices = 6

MaxSlices = 2048

-- END cluster.ini

* Modify virtuoso.ini parameters according to openlink specifications virtuoso_optimized.ini
	- note that the number of HTTP threads has an effect on the bulk loading possibilities, license allows 10 client connections
	- to benchmark the query performance load the data with 1 bulk loader per node and 9 HTTP threads in the master node
	- to test load performance: set the number of http threads to a smaller value so we can run 9 bulk loader scripts per node (<7 HTTP connection)

* Start the cluster nodes, first slaves than master:
	- `sudo bash bin/virtuoso-start.sh`
	- is it alive? `top -b | grep virtuoso`

* Cluster status checks (master)
	- check logs voor PL_Log line: `xx:xx:xx PL LOG: Elastic cluster setup`
	- 
	- `sudo bin/isql 12201 dba dba exec="status ('cluster_d');"`
	- `sudo bin/isql 12201 dba dba exec="cl_ping(1,500,1000;"` (ping node 1)
	- OTHER:
		- Definitely make a **checkpoint** after bulkloading: `sudo ./bin/isql 12201 exec="cl_exec('checkpoint')"`
		- Cluster shutdown? `sudo ./bin/isql 12201 exec="cl_exec('shutdown');"`

* `screen` (it might be useful to use screen sessions, Ctrl a-d to detach from a screen, for example with the bulk loader, ctrl-C cancels this process!)

* for every node een run ld_dir, followed by bulkload.sh (3 threads for bulk loading)
`
`sudo bin/isql 12201 dba dba exec="ld_dir('../data', '*.nq.gz', 'http://watdiv.com');"`
`sudo bin/isql 12202 dba dba exec="ld_dir('../data', '*.nq.gz', 'http://watdiv.com');"`
`sudo bin/isql 12203 dba dba exec="ld_dir('../data', '*.nq.gz', 'http://watdiv.com');"`

* start bulkload.sh (important: script should include a checkpoint!), **IMPORTANT** change the port in the script per node, run the script on every node! (you can modify the number of rdfloaders!)

* some tests to check if virtuoso is working properly:
`sudo bin/isql 12201 dba dba exec="select * from DB.DBA.load_list;"`
	- `sudo bin/isql 12201 dba dba exec="select * from DB.DBA.load_list;"`
	- `sudo bin/isql 12201 dba dba exec="sparql select count(*) where {?s ?p ?o};"`
		* ll_state 1 = in progress, 2 finished

	- *** Error 08004: VD [Virtuoso Server]LI100: Number of licensed connections exceeded => go to ip masternode  http://ec2-52-87-187-104.compute-1.amazonaws.com:8890/conductor/
	- go to database interactive sql  => select * from DB.DBA.load_list;

* Canceling, resetting?
	- reset store: `sudo bin/isql 12201 dba dba exec="RDF_GLOBAL_RESET();"`
	- stop bulk loader: `sudo bin/isql 12201 dba dba exec="rdf_load_stop(1);"`
	- kill a server: `sudo bin/isql 12201 dba dba -K`
	- remove lines bulk loading list:  `sudo bin/isql 12201 dba dba exec="DELETE FROM DB.DBA.load_list;"`
	- `sudo /etc/init.d/virtuoso restart`



# Notes on simulations

First Virtuoso Cluster Simulation Crashed after about half an hour. 
Remove all database files, restart cluster and restart bulk loading process






