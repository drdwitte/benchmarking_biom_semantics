
# coding: utf-8

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

#docker share directory (/home/dockeruser/benchmarkoutput)
outputdir = 'benchmarkoutput/'

#make outputfiles unique per run and simulation
def decorateFilename(name, run_id, timestamp, extension):
        fname = "%s_%s_%s" % (name, run_id, timestamp)
	return fname + extension

#define runner command
def run(no):

	init_timestamp_str =  str(int(time.time()))

	general_command = ["./benchmark", \
		"-m", queryListName, \
		"-r", str(runs), \
		"-o", str(outliers), \
		"-w", str(warmups), \
		"-q", endpoint, \
		"-p", str(parallell), \
		"-c", outputdir + decorateFilename(resultsFile, no, init_timestamp_str, ".csv"), \
		"-t", str(timeout), \
		"--log-file", outputdir + decorateFilename("runner", no, init_timestamp_str, ".log") \
		]

	auth_command = ["./benchmark", \
		"-m", queryListName, \
		"-r", str(runs), \
		"-o", str(outliers), \
		"-w", str(warmups), \
		"-q", endpoint, \
		"-p", str(parallell), \
		"-c", outputdir + decorateFilename(resultsFile, no, init_timestamp_str, ".csv"), \
		"-t", str(timeout), \
		"--username", user, \
		"--password", pwd, \
		"--log-file", outputdir + decorateFilename("runner_"+store, no, init_timestamp_str,".log"), \
		]

    	if results_dir is not None:
		general_command.append("--store-results-dir")
		general_command.append(outputdir + decorateFilename(str(results_dir)+"_"+store,no,init_timestamp_str ,""))

		auth_command.append("--store-results-dir")
		auth_command.append(outputdir + decorateFilename(str(results_dir)+"_"+store,no,init_timestamp_str ,""))
    
		
	if requiresAuth:
	        print ("requires auth")
		print (" ".join(auth_command))

        	return subprocess.Popen(auth_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		

    	else:
		print (" ".join(general_command))
        	return subprocess.Popen(general_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def trace(proc):
	while proc.poll() is None:
        	line = proc.stdout.readline()
        	if line:
            		# Process output here
            		logger.info('STATUS: %s' % line)

          

#function used for polling if dataset is fully loaded           
def hasTriple(sparql, triple):

    	if not triple:
		print('No ASK query checks')
		return True

    	query = "ASK { %s %s %s }" % (triple[0], triple[1], triple[2])
    	print(query)
    
    	if requiresAuth:
        	response = requests.get(sparql.endpoint + '?format=json&query=%s' % urllib.quote_plus(query)  + additional_request_str, auth=HTTPBasicAuth(user, pwd))
    	else:
        	response = requests.get(sparql.endpoint + '?format=json&query=%s' % urllib.quote_plus(query) + additional_request_str)
   
    
    	results = response.json()
    
    	if type(results) is bool :
        	return results
    	else:
        	return results['boolean']        
        

#parsing yaml config file to be able to generate runner command
def main(argv):
    	global logger, resultsFile, requiresAuth, user, pwd, queryListName, queries, runs, outliers, warmups, parallell, endpoint, timeout, results_dir,  additional_request_str, store
    
    	#additional_request_str = '&Accept=application%2Fsparql-results%2Bjson' for Ontotext GraphDB simulations

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

    	if  not configfile:
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
    
    	#Store under test
    	if not 'storeUnderTest' in config:
		print('simulation name missing, add storeUnderTest: parameter in YAML file')
        	sys.exit(2)

    	store = config['storeUnderTest']

    	#Log file
    	logger = logging.getLogger('Logger')
    	fhandler = logging.FileHandler(filename=outputdir + "output_"+store+".log", mode='a')
    	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    	fhandler.setFormatter(formatter)
    	logger.addHandler(fhandler)
    	logger.setLevel(logging.DEBUG)
    	logger.propagate = False

    

	#Runner
	totalRuns = config['totalRuns'] if 'totalRuns' in config else 1 #1 immediate, one after fixed time, one control run after same time interval
	timeInterval = config['timeInterval'] if 'timeInterval' in config else 1 #in seconds

    	#Target Endpoint
    	if not 'endpoint' in config:
		print('sparql endpoint missing, add endpoint: parameter in YAML file')	
		sys.exit(2)

	endpoint = config['endpoint']
	sparqlEndpoint = SPARQLWrapper(endpoint)
	requiresAuth = config['requiresAuth'] if 'requiresAuth' in config else False

    	user = config['user'] if 'user' in config else None
    	pwd = config['pwd'] if 'pwd' in config else None

    	if requiresAuth:
        	sparqlEndpoint.setCredentials(user, pwd)

    	#Dataset
    	firstTriple = config['firstTriple'] if 'firstTriple' in config else None
    	lastTriple = config['lastTriple'] if 'lastTriple' in config else None

    	#Queries
    	if 'queryListName' not in config:
		print ('querylist file missing in config add queryListName: parameter in YAML file')
        	sys.exit(2)
	
    	queryListName = config['queryListName'] #should crash if missing

    	#Benchmark
    	runs = config['runs'] if 'runs' in config else 5
    	outliers = config['outliers'] if 'outliers' in config else 0
    	warmups = config['warmups'] if 'warmups' in config else 1
    	parallell = config['parallell'] if 'parallell' in config else 1
    	resultsFile = "results_"+store
    	timeout = config['timeout'] if 'timeout' in config else 300
    	results_dir = config['results_dir'] if 'results_dir' in config else None    	
        
    	#Retrieve the queries
    	if not os.path.isfile(queryListName):
        	print ("Cannot find querylist file: " + queryListName)
		sys.exit(2)

    	else:
        	print ("Query list found!")

   
    	additional_request_str = config['additional_request_str'] if 'additional_request_str' in config else ""

    	#Test if the endpoint is up and data is loaded and execute run

    	while ( not hasTriple(sparqlEndpoint, firstTriple) ) or (not hasTriple(sparqlEndpoint, lastTriple) ):
        	logger.info("This polls once a minute until data is loaded.")
        	time.sleep(60)
    
    	logger.info("All data is loaded.")
    	print("All data is loaded.")

    	logger.info("Running Queries")
    	print("Running Queries")

    	logger.info("Run %s of %s" % (0+1, totalRuns))
    	print("Run %s of %s" % (0, totalRuns))

    	rProc = run(0)
    	trace(rProc)

    	for x in range(1, totalRuns):

		logger.info("Waiting %s for next run" % (timeInterval))
		print("Waiting %s for next run" % (timeInterval))
    		time.sleep(timeInterval)

        	logger.info("Run %s of %s" % (x+1, totalRuns))
        	print("Run %s of %s" % (x, totalRuns))

        	rProc = run(x)
        	trace(rProc)

    	

	if results_dir is not None:
		print("Moving query hashmappings file queryname_hashmappings.log to benchmarkoutput/queryname_hashmappings_"+ store + ".log")
		hash_filename = "queryname_hashmappings.log"
		shutil.move(hash_filename, "benchmarkoutput/queryname_hashmappings_" + store + ".log")
 
	pass



if __name__ == "__main__":
	main(sys.argv[1:])







