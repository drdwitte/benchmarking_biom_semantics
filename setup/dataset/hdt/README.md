
# Docker container for HDT compression

https://hub.docker.com/r/rfdhdt/hdt-cpp/

* `sudo docker run -it --rm rfdhdt/hdt-cpp rdf2hdt -h`

* RDF to hdt:
	- `sudo docker run -it --rm -v $(pwd):/data rfdhdt/hdt-cpp rdf2hdt -f turtle /data/myfile.turtle /data/myfile.hdt`
	- -f <format>	Format of the RDF input (ntriples, nquad, n3, turtle, rdfxml)

-  **only turtle format works currently** (turtle is a superset of ntriples)


## watdiv.1000M.nt

* watdiv.1000M.nt is 159 GB in size
* attempt to make on hdt file out of this?
	- sudo docker run -it --rm -v $(pwd):/data rfdhdt/hdt-cpp rdf2hdt -f ntriples /data/watdiv.1000M.nt /data/watdiv.1000M.hdt &
	- doesn't work

* split in 3 files of 333M triples and in 12 files of approx 80M triples.
	- watdiv.333M.nt => watdiv.333M.hdt (Time: 1h10m4seconds x 3)
	- watdiv.80M.nt => watdiv.80M.hdt (Time: 17 minutes 13 sec)

## watdiv.100M.nt

* single hdt file 
	- watdiv.100M.nt -> watdiv.100M.hdt (Time:  13m 28 seconds)

* partition in 3 parts => 3 hdt files for federated tests
	- watdiv.33M.nt -> watdiv.33M.hdt (Time: 4 min 44 seconds x3)



