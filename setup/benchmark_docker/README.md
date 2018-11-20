### Build docker instance

* Note: This takes a couple of minutes since it also runs a small benchmark against sparql.org

* `sudo docker build -t drdwitte/benchmarker .`
* `sudo docker run -it --name benchmarker -v $(pwd)/benchmarkoutput:/home/dockeruser/benchmarkoutput drdwitte/benchmarker`

* attach a shell to the running container: `sudo docker exec -it benchmarker /bin/bash`

### Run benchmark

* put the queries directory and querylist file in your shared directory, after booting the docker container move the querylist file to /home/dockeruser, note that the listfiles
should contain absolute paths or paths relative to the querylistfile (/home/dockeruser)

* navigate to the home directory in your docker container shell: `/home/dockeruser/`

* `python BenchmarkRunnerDocker.py -c generalconfig.yaml &` (Ctrl-C to detach)

* after finishing the benchmark all benchmark related data and logs are stores in the shared directory benchmarkoutput. 

### Contents of the config.yaml file

#### 1. Required parameters

* Name of simulation (used in log and results files, should be unique):
	- `storeUnderTest: "VirtuosoVirtualWallTest"`
* SPARQL endpoint to query:
	- `endpoint: "http://193.193.193.193:8890/sparql/"`

* File with paths to query files (NOTE: 1 query per file):
	- `queryListName: "listfiles.txt"`
  
#### 2. Required parameters with default values

* Number of full benchmark runs (generally 1 is recommended)
	- `totalRuns: 1`
* Amount of time (seconds) between two consequent full benchmark runs
	- `timeInterval: 1`
* For SPARQL endpoints which require authentication:
	- `requiresAuth: False`
* Query timeout parameter:
	- `timeout: 300`

* Number of query mixes to run (query mix =  all queries executed by a single thread in randomized order):
	- `runs: 5`

* Number of warmup runs prior to actual runs:
	- `warmups: 1`

* Maximal number of parallel threads (note: the actual maximum is also influenced by the number of available query mixes):
	- `parallell: 8`

* Number of results per query run that can be omitted as outliers (for results.csv file time calculations)
	- `outliers: 0`

#### 3. Optional parameters
	
* Login credentials in case authentication is required: 
	- `user: "dba"`
	- `pwd: "dba"`	

* If the triple store is not finished loading and we want to immediately start after finish loading we can provide the benchmarker with the first and the last triple of the RDF dataset. It will fire
ask queries every minute and delay the benchmarking until both triples are loaded succesfully:

	`firstTriple:`
	`  - "<http://db.uwaterloo.ca/~galuc/wsdbm/User0>"`
	` - "<http://schema.org/email>"`
	`  - "\"Maggie's serialization's Brunhilde blunderers urinalyses\""``

	`lastTriple:`
	`  - "<http://db.uwaterloo.ca/~galuc/wsdbm/Review14999999>"`
	`  - "<http://purl.org/stuff/rev#reviewer>"`
	`  - "<http://db.uwaterloo.ca/~galuc/wsdbm/User9776014>"`  

* Sparql benchmarker was extended with the option to store the actual query results, adding this parameter to the yaml file will generate a file for every query that has been exectured. The foldername will be decorated with the run_id and a timestamp to avoid name collisions in reruns:
	- `results_dir: "SparqlResults"`

### Remarks about extensions

The Sparql Benchmarker code was modified to allow an extra parameters `--store-results-dir`. This folder will contain the results of a SPARQL query, and this for every time it is executed in a query mix. Since the queryname is not available in the source code at the moment of query execution we chose the following approach:

- the actual SPARQL query is hashed -> sparqlHash
- at the moment of execution of a query the timestamp is taken -> queryTime
- This leads to a file with the following naming convention: `sparqlHash_queryTime.log`
- The number of files with the same prefix should therefore correspond to #warmups + #runs
- Note that for the Watdiv benchmark the queries are generated by a randomized algorithm, therefore duplicates might be present, in that case the number of result files is n x #warmups + #runs