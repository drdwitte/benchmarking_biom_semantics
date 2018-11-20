# LDF 

## A. Setup of LDF server with nginx cache



- https://github.com/LinkedDataFragments/FullStackServer
- modifications:
	* 8 cores!
		- `worker_processes 8; ` in nginx.conf
- DATA_DIR and LDF_WORKERS can be set in .env file! => workers should be 8

- prereqs: 
	- install docker-compose: https://docs.docker.com/compose/install/ (requires Docker Engine 1.10.0 or later)
		- `sudo apt-get install curl`
		- `sudo -i` (you should install as a superuser)
		- `curl -L https://github.com/docker/compose/releases/download/1.9.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose`
		- `chmod +x /usr/local/bin/docker-compose`

- download full stack server (ldf-server + nginx + ldfwebclient):
	- `git clone https://github.com/LinkedDataFragments/FullStackServer.git`
        - modify config.server.json, config.client.json and nginx.conf and .env file LDF_WORKERS = 8
	- run as daemon: `sudo docker compose up -d &`
- check if successfully started at: http://localhost:3000/watdiv1, http://localhost:3000/watdiv2 and http://localhost:3000/watdiv3 

- Note client widget not working in this current version but client is running in a different container

- creating .index files for every .hdt file takes some time: 
	- Time for all index files to be generated: 
		- Watdiv1000M (LDF N1) `Index generated in 19 min 19 sec 336 ms 599 us`
		- Watdiv100M (LDF N1) `Index generated in 1 min 21 sec 291 ms 128 us`		
		- Watdiv100M (LDF N3) `Index generated in 23 sec 82 ms 765 us`
		- Watdiv1000M (LDF N3) `Index generated in 6 min 116 ms 160 us`

## B. LDF http client

- `sudo docker pull node`
- `sudo docker run -p 1234:1234  --name ldfclient -it node /bin/bash`

- build from source:
	- `git clone https://github.com/LinkedDataFragments/Client.js.git`
	- `cd Client.js`
 	- `npm install .`
	- `bin/ldf-client-http http://<ip>:80/watdiv1 http://<ip>:80/watdiv2 http://<ip>/watdiv3 -p 1234 -t 301`
	- client at <ip>:1234, 
	- sample query: `http://localhost:1234/sparql?query=select%20distinct%20%3Ftype%20where%20{%0A%3Fthing%20a%20%3Ftype%0A}%0Alimit%2020`
	
# 
#`bin/ldf-client-http http://193.190.127.241/watdiv1 http://193.190.127.241/watdiv2 http://193.190.127.241/watdiv3 -p 1234 -t 301`

Interesting tip to do the url encoding:
* `curl -G http://193.190.127.240:1234/sparql --data-urlencode query='select * where {?s ?p ?o} limit 10'
`
* Run a number of queries about a subject unique to one of the fragments:
	- frag1: `curl -G http://193.190.127.240:1234/sparql --data-urlencode query='select * where { <http://db.uwaterloo.ca/~galuc/wsdbm/Offer1000047> ?p ?o}' `
	- frag2: `curl -G http://193.190.127.240:1234/sparql --data-urlencode query='select * where { <http://db.uwaterloo.ca/~galuc/wsdbm/Offer1000167> ?p ?o}' `
	- frag3: `curl -G http://193.190.127.240:1234/sparql --data-urlencode query='select * where { <http://db.uwaterloo.ca/~galuc/wsdbm/Offer100306> ?p ?o}' `


test watdiv100: 

`curl -G http://193.190.127.244:1234/sparql --data-urlencode query='select * where { <http://db.uwaterloo.ca/~galuc/wsdbm/Offer10> ?p ?o}' `
`curl -G http://193.190.127.244:1234/sparql --data-urlencode query='select * where { <http://db.uwaterloo.ca/~galuc/wsdbm/City0> ?p ?o}' `



## C. setup benchmarker

- sparql endpoint: http://193.190.127.240:1234/sparql


curl -G http://193.190.127.240:1234/sparql --data-urlencode query='ASK WHERE { ?s ?p ?o } '`





SELECT ?v0 ?v4 ?v6 ?v7 WHERE { ?v0 <http://schema.org/caption> ?v1 . ?v0 <http://schema.org/text> ?v2 . ?v0 <http://schema.org/contentRating> ?v3 . ?v0 <http://purl.org/stuff/rev#hasReview> ?v4 . ?v4 <http://purl.org/stuff/rev#title> ?v5 . ?v4 <http://purl.org/stuff/rev#reviewer> ?v6 . ?v7 <http://schema.org/actor> ?v6 . ?v7 <http://schema.org/language> ?v8 .
}

