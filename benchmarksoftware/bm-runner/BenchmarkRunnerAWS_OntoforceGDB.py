
# coding: utf-8

# In[6]:

import os
import logging
import os.path
import subprocess
from subprocess import STDOUT
from SPARQLWrapper import SPARQLWrapper, JSON
import wget
import tarfile, sys, getopt
import time
import gzip
import shutil
import requests
from requests.auth import HTTPBasicAuth
import urllib
import yaml


# Define the Runner Commands
# ------------------------------

# In[7]:

def run(no):
    print(["./sparql-query-bm-2.1.0/cmd/benchmark", "-m", "./%s" % queryListTxt, "-r", str(runs), "-o", str(outliers), "-w", str(warmups), "-q", endpoint, "-p", str(parallell), "-t", "1200", "-c", "./%s_%s_%s.csv" % (resultsFile, no, str(int(time.time()))), "--log-file", "runner.log"])
    if requiresAuth:
        print ("requires auth")
        return subprocess.Popen(["./sparql-query-bm-2.1.0/cmd/benchmark", "-m", "./%s" % queryListTxt, "-r", str(runs), "-o", str(outliers), "-w", str(warmups), "-q", endpoint, "-t", "1200", "-p", str(parallell), "-c", "./%s_%s_%s.csv" % (resultsFile, no, str(int(time.time()))), "--username", user, "--password", pwd,  "--log-file", "runner.log"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        return subprocess.Popen(["./sparql-query-bm-2.1.0/cmd/benchmark", "-m", "./%s" % queryListTxt, "-r", str(runs), "-o", str(outliers), "-w", str(warmups), "-q", endpoint, "-t", "1200", "-p", str(parallell), "-c", "./%s_%s_%s.csv" % (resultsFile, no, str(int(time.time()))), "--log-file", "runner.log"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def trace(proc):
    while proc.poll() is None:
        line = proc.stdout.readline()
        if line:
            # Process output here
            logger.info('STATUS: %s' % line)


# In[8]:

def untar(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print ("Extracted in Current Directory")
    else:
        print ("Not a tar.gz file: " + str(sys.argv[0]))
        
def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])
        elif item.name.find(".gz") != -1:
            outFilePath = item.name[:-3]
            decompressedFile = gzip.open(item.name, 'r')
            with open(outFilePath, 'w') as outfile:
                outfile.write(decompressedFile.read())
            decompressedFile.close()
            os.remove(item.name)
            

            
def hasTriple(sparql, triple):
    query = "ASK { %s %s %s }" % (triple[0], triple[1], triple[2])
    print(query)
    
    if requiresAuth:
        response = requests.get(sparql.endpoint + '?format=json&query=%s' % urllib.quote_plus(query), auth=HTTPBasicAuth(user, pwd))
    else:
        response = requests.get(sparql.endpoint + '?format=json&query=%s' % urllib.quote_plus(query) + '&Accept=application%2Fsparql-results%2Bjson')
   
    
    print(response.text)    
    results = response.json()
    
    if type(results) is bool :
        return results
    else:
        return results['boolean']        
        


# In[10]:

def main(argv):
    global logger, resultsFile, requiresAuth, user, pwd, queryListTxt, queries, runs, outliers, warmups, parallell, endpoint
    
    configfile = False
    config = False
    # Read Config file
    try:
        opts, args = getopt.getopt(argv,"hc:",["config="])
    except getopt.GetoptError:
        print ('test.py -c <configfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -c <configfile>')
            sys.exit()
        elif opt in ("-c", "--config"):
            configfile = arg

    if not configfile:
        print ('No config file given, usage:')
        print ('test.py -c <configfile>')
        sys.exit(2)
    else:
        print ('Config file is "', configfile)
        config = yaml.safe_load(open(configfile))
        
    if not config or config is None:
        print ('Invalid config file given, try again or check the path to the config file, usage:')
        print ('test.py -c <configfile>')
        sys.exit(2)
    else:
        print ('Loaded config')
        print (config)
        
    
    ##Set Benchmarker Parameters
    
    #Log file
    logger = logging.getLogger('Logger')
    fhandler = logging.FileHandler(filename='output.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    #Store under test
    store = config['storeUnderTest']

    #Runner
    url = "http://downloads.sourceforge.net/project/sparql-query-bm/2.1.0/sparql-query-bm-distribution.tar.gz"
    fname = "sparql-query-bm-distribution.tar.gz"
    dirname = "sparql-query-bm-2.1.0"
    totalRuns = config['totalRuns'] #1 immediate, one after fixed time, one control run after same time interval
    timeInterval = config['timeInterval'] #in seconds
    checkDataLoaded = config['check_data_loaded']

    #Target Endpoint
    endpoint = config['endpoint']
    sparqlEndpoint = SPARQLWrapper(endpoint)
    requiresAuth = config['requiresAuth']

    user = config['user']
    pwd = config['pwd']

    if requiresAuth:
        sparqlEndpoint.setCredentials(user, pwd)

    #Dataset
    firstTriple = config['firstTriple']

    lastTriple = config['lastTriple']

    #Queries
    queryListName = config['queryListName']
    queryList = config['queryListSource'] + queryListName 
    queryListTxt = queryListName[:-3]+"txt"
    queriesName = config['queriesName']
    queries = config['queryListSource'] + queriesName + ".tar.gz"

    #Benchmark
    runs = config['runs']
    outliers = config['outliers']
    warmups = config['warmups']
    parallell = config['parallell']
    resultsFile = "results_"+store
    
    
    #Install if necessary the Benchmarker Software
    if not os.path.isfile(fname):
        print ("Downloading: " +  str(fname))
        wget.download(url)
    if not os.path.isdir(dirname):
        print ("Untarring to dir: " + str(dirname))
        untar(fname)
    else:
        print ("SPARQL Benchmarker already present in dir: " + str(dirname))
        
        
    #Retrieve the queries
    if not os.path.isfile(queryListName):
        print ("Downloading: " +str(queryListName))

        print("wget: " + str(queryList))
        wget.download(queryList)
    else:
        print ("Query list already present: " + str(queryListName))

    if not os.path.isfile(queryListTxt):
        shutil.copyfile(queryListName, queryListTxt)

    if not os.path.isfile(queriesName + ".tar.gz"):
        print ("Downloading: " + str(queriesName))
        wget.download(queries)
    if not os.path.isdir(queriesName):
        print ("Untarring to dir: " + str(queriesName))
        extract(str(queriesName) + ".tar.gz")
    else:
        print ("Queries already present in dir: " + str(queriesName))    
    
    
    #Test if the endpoint is up and data is loaded and execute run
    time.sleep(30)

    if checkDataLoaded:
        while ( not hasTriple(sparqlEndpoint, firstTriple) ) or (not hasTriple(sparqlEndpoint, lastTriple) ):
            logger.info("This polls once a minute until data is loaded.")
            time.sleep(60)
    
    logger.info("All data is loaded.")
    print("All data is loaded.")

    logger.info("Running Queries")
    print("Running Queries")

    for x in range(0, totalRuns):
        logger.info("Run %s of %s" % (x, totalRuns))
        print("Run %s of %s" % (x, totalRuns))

        rProc = run(x)
        trace(rProc)

        logger.info("Waiting %s for next run" % (timeInterval))
        print("Waiting %s for next run" % (timeInterval))

        time.sleep(timeInterval)   


# In[ ]:

#run as a script
isNotebook = False

if not isNotebook:
    if __name__ == "__main__":
        main(sys.argv[1:])
else:
    main(['-c','configfile.txt'])


# In[ ]:



