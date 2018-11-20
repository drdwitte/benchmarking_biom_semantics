# Docker image created for fuseki hdt installation 

* `sudo docker build -t drdwitte/fusekihdt .`
* `sudo docker run -it --name fusekihdt -p 3030:3030 -v $(pwd)/data:/data drdwitte/fusekihdt`

* modifications: bin/hdtEndpoint.sh we increased the jvm heap space to 64 GB 
* we added an example config used for watdiv: ./fuseki_watdiv.ttl

* download the hdt datasets to /data (this is a shared between docker container and container host!

* start the endpoint as follows:
	- sudo chmod 777 bin/hdtEndpoint.sh
	- `bin/hdtEndpoint.sh --config=fuseki_watdiv.ttl >> fuseki.log &`
	- note that fuseki will generate .index files for every hdt file, this time has to be added to the loading time (fuseki loading  time: time to create hdt + time to create hdt.index files)

	- 10 min 28 to create .index files for watdiv.1000M
	- 1m 48 for watdiv.100M


* benchmark sparql endpoint at:
	http://<ip>:3030/hdtservice/query
	193.190.127.237
   	ofwel query ipv sparql?

* Note issues with timeout parameter for fuseki hdt => throws exception!
