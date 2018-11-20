
# Setup FluidOps (FedX)

* FluidOps Workbench contains FedX which federates SPARQL queries to a set of endpoints, this requires N + 1 nodes for the simulation: 
	- N SPARQL endpoints
	- 1 FedX node which will combine the results of the different endpoints to resolve the queries
	- We run 2 simulations, one with N=1 (query forwarding) and one with N=3 slaves
 
* Video at https://www.youtube.com/watch?v=k73gq7hPsFM

* Prerequisites:
   - java 8
   - ubuntu 14

* Install FluidOops Workbench downloaded at (create a free account): `https://appcenter.fluidops.com/resource/Download` (linux platform)



* Download the Virtuoso Adapter Plugin(also in github) : `virtuoso-bridge.zip` => put all files in the corresponding folders in the FluidOps project
        - `wget https://github.com/drdwitte/rdfbenchmarking/raw/master/setup/endpoints/FluidOps/virtuoso-bridge.zip`

* Download the FedX plugin (in github we have pre-release version 3.2)
        - `wget https://github.com/drdwitte/rdfbenchmarking/raw/master/setup/endpoints/FluidOps/fedx-3.1.2.jar`
	- shortcut for internal use: download from s3://... /fedxinstaller/*

* Unzip archives:
	- `unzip fluidOps-Suite_v7.1.0.2993.zip` 
	- `mkdir virtuoso-bridge && mv virtuoso-bridge.zip ./virtuoso-bridge && cd virtuoso-bridge && unzip virtuoso-bridge.zip`

* java8:
    - prereq: `sudo apt-get install software-properties-common`
    - `sudo add-apt-repository ppa:webupd8team/java`
    - `sudo apt-get update`
    - `sudo apt-get install oracle-java8-installer`
    - `java -version`

* Move fedx-3.1.2.jar to ~/fluidOps-Suite/lib and remove the original fedx-3.1.jar:

* Move Virtuoso Adapter files to corresponding dirs in workbench:

	- `cp ./virtuoso-bridge/config/repositories/templates/* ./fluidOps-Suite/config/repositories/templates/`
	- `cp -r ./virtuoso-bridge/data/wikiBootstrap/ ./fluidOps-Suite/data/wikiBootstrap/`
        - `cp -r ./virtuoso-bridge/lib/extensions/ ./fluidOps-Suite/lib/extensions/`
        - `cp ./virtuoso-bridge/solution.properties ./fluidOps-Suite/solution.properties`
        - `cp ./virtuoso-bridge/virtuoso-bridge.zip ./fluidOps-Suite/virtuoso-bridge.zip`

* Further Installation instructions at `~/fluidOps-Suite/ReadMe.html`
    - `sudo bash -eu linux-install.sh drdwitte` (user drdwitte)
    - starting the workbench as follows: `/etc/init.d/fops start`
    - access workbench at https://localhost:50443 (WARNING: it's https not http!)
    - admin/iwb are user/pwd for sparql!
    - http://localhost:50080/sparql => http endpoint!

* admin/iwb are user/pwd for sparql!

* Allow passwordless access:
    - putting a file "role-publicSparqlEndpoint.acl" into the "config/acl/extensions/" folder of your installation
    - content: 
        * ### Extension role ###
        * @includeRole: sparql-query
        * @includedByRole: guest

    - Note since the dir extensions is missing, duplicate the file to one dir higher (which contains all .acl files, it's unclear what the real location is for the new .acl file)

* Enable HTTP access: the "enableHttp" setting on the system configuration page "resource/Admin:Config", set the value to true (go to settings/ system configuration / security)

* configure query timeout! (Admin:Config / Database)
    - queryTimeout 300

* **PERFORMANCE CORRECTION:**
    - FedX on 3 nodes is stops responding and is constantly timing out => logs show continuous garbage collection => too little heap!
        * Java memory is too low => ~/backend.conf 
        * from docs.oracle.com => heap size 80% of available memory and 'in production environment set min = max heapsize to avoid wasting resources resizing the heap 
        * 50GB makes sense for heap size!
        * `wrapper.java.additional.10=-Xmx50G`
        * `wrapper.java.additional.11=-Xms50G`
        * `wrapper.java.additional.40=-XX:+UseG1GC` (recommended gc parameter)

* restart the workbench: 
    - `/etc/init.d/fops stop`
    - `/etc/init.d/fops start`



* Go to Admin:RepositoryManagement -> create 'virtuoso' repository (if adapter is installed this should be possible!)

* FedX_VirtN1: (and select as federated!)
    - Repository ID: `FedX_VirtN1`
    - Host list: `ip_virtuoso_node:1111`

* FedX_VirtN3: (and select as federated!)
    - Repository ID: `FedX_VirtN3_1`
    - Host list: `ip_virtuoso_node1:1111`
    - Repository ID: `FedX_VirtN3_2`
    - Host list: `ip_virtuoso_node2:1111`
    - Repository ID: `FedX_VirtN3_3`
    - Host list: `ip_virtuoso_node3:1111`

* Test all repos! (TROUBLESHOOTING: is port 1111 opened at Virtuoso?)

* Tested if connection  is good by running a SPARQL query:
	- `select distinct ?s where { ?s ?p ?o } LIMIT 100 OFFSET  1000` (added offset otherwise only virtuoso system triples, now productid subjects pop up)

* Benchmarker setup:
    - `endpoint            : "http://193.190.127.244:50080/sparql?repository=federated"`   
    - `requiresAuth     : False`
    - `user                     : "admin"`
    - `pwd                      : "iwb"`





