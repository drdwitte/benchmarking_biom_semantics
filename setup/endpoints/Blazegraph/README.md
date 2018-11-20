# Installation instructions

* Install docker container requires several steps: 
    - `git clone https://github.com/laurensdv/docker-blazegraph.git`
    - `cd docker-blazegraph/`	
    - `sudo docker build -t blazegraph:2.1.2 2.1.2/`
    - `sudo docker run -it --name blazegraph -p 9999:9999 -v $(pwd)/data:/data_mount/data blazegraph:2.1.2`

* The shared folder `/data_mount/data` contains all the source data.
This means that after breaking the container Blazegraph could be restored by reloading the data using the same procedure. If need be, the blazegraph journal file: `bigdata.jnl` could be copied to `/data_mount/data` for backup and restored by copying it to `/` on the running docker container.

* ISSUE in container: errors related to terminal can be solved by: `export TERM=xterm`, you have to run this every time you connect to the container

* Extra software: nano text editor for editing config files: `apt-get install nano`
  
# Configuration of Blazegraph

* The github contains a file called `RWStore.properties`, this allows the user to modify to suit own needs.

* This file is already optimized, according to the <a href=""https://wiki.blazegraph.com/wiki/index.php/PerformanceOptimization>documentation, specific for benchmarking purposes. </a>

# Blazegraph Bulk Loader

* After starting the docker machine

*  put the data in the mounted directory

* `java -cp *:*.jar com.bigdata.rdf.store.DataLoader /RWStore.properties /data_mount/data/`

# Blazegraph Sparql Endpoint

* `java -server -Xmx64g -jar blazegraph.jar` (do not use all available memory, some needs to be available for garabage collection, follow https://wiki.blazegraph.com/wiki/index.php/Hardware_Configuration#RAM_Sizing_Guidance)

* If you want to set the server-side time out you need to override the web.xml as follows by adding a web.xml file

`-Djetty.overrideWebXml=web.xml`

```<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_1.xsd"
      version="3.1">
  <context-param>
   <description>When non-zero, the timeout for queries (milliseconds).</description>
   <param-name>queryTimeout</param-name>
   <param-value>301000</param-value>
  </context-param>
</web-app>```


- `java -server -Xmx56g -jar blazegraph.jar Djetty.overrideWebXml=web.xml`

- endpoint: `curl -G http://193.190.127.244:9999/blazegraph/namespace/kb/sparql --data-urlencode query='select * where { ?s ?p ?o } limit 10'`

- NOTE it's possible to create a different namespace (than kb) with different properties via the UI

