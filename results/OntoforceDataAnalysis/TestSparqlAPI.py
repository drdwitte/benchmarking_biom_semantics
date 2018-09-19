
# coding: utf-8

# In[1]:

from SPARQLWrapper import SPARQLWrapper, JSON


# <b> Documentation of wrapper</b>
# http://rdflib.github.io/sparqlwrapper/doc/latest/

# In[2]:

queryString = "SELECT * WHERE { ?s ?p ?o. } LIMIT 1000"
sparql = SPARQLWrapper("http://localhost:8000/sparql/")
sparql.setQuery(queryString)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
#print ("subject \t predicate \t object")
for result in results["results"]["bindings"]:
    t1 = str(result['s']['value'])
    t2 = str(result['p']['value'])
    t3 = str(result['o']['value'])

    #print(t1[27:] + '\t' + t2[33:] + '\t' +t3[27:])


# Some stats queries from: https://code.google.com/p/void-impl/wiki/SPARQLQueriesForStatistics

# <b> 1. total number of triples <b>

# In[3]:

def performSparqlQuery(queryStr):
    sparql.setQuery(queryStr)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']

queryString ="SELECT (COUNT(*) AS ?numtriples) { ?s ?p ?o  }"
results = performSparqlQuery(queryString)

print (results[0]['numtriples']['value'])


# <b>2. total number of entities</b>

# In[4]:

#added brackets, otherwise query was failing if COUNT instead of (COUNT ... )
queryString ="SELECT (COUNT(distinct ?s) AS ?numsubjects) { ?s a []  }"
results = performSparqlQuery(queryString)

print (results[0]['numsubjects']['value'])


# <b> 3. total number of distinct classes </b>

# In[5]:

queryString = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT (COUNT(distinct ?o) AS ?distinctclasses) { ?s rdf:type ?o }
"""
results = performSparqlQuery(queryString)

print (results[0]['distinctclasses']['value'])


# <b> 4. total number of distinct predicates </b>

# In[6]:

queryString = """
SELECT (COUNT(distinct ?p) as ?distpredicates) { ?s ?p ?o }
"""
results = performSparqlQuery(queryString)

print (results[0]['distpredicates']['value'])


# <b> 5. total number of distinct subject nodes </b>

# In[14]:

queryString = """
SELECT (COUNT(DISTINCT ?s ) AS ?distsubjects) {  ?s ?p ?o   } 
"""
results = performSparqlQuery(queryString)

print (results[0]['distsubjects']['value'])


# <b> 6. total number of distinct object nodes  </b>

# In[16]:

queryString = """
SELECT (COUNT(DISTINCT ?o ) AS ?distobjects) {  ?s ?p ?o  filter(!isLiteral(?o)) } 
"""
results = performSparqlQuery(queryString)

print (results[0]['distobjects']['value'])


# <b> 7. exhaustive list of classes used in the dataset </b>

# In[18]:

queryString = """
SELECT DISTINCT ?type { ?s a ?type }
"""
results = performSparqlQuery(queryString)

print (results)


# <b> 8.  exhaustive list of properties used in the dataset </b>

# In[22]:

queryString = """
SELECT DISTINCT ?p { ?s ?p ?o }
"""
results = performSparqlQuery(queryString)

for c in results:
    print (c['p']['value'])



# <b> 9. table: class vs. total number of instances of the class </b>

# In[24]:

queryString = """
SELECT  ?class (COUNT(?s) AS ?count ) { ?s a ?class } GROUP BY ?class ORDER BY ?count
"""
results = performSparqlQuery(queryString)

for c in results:
    print (c['class']['value'])
    print (c['count']['value'])



# <b> 10. table: property vs. total number of triples using the property   </b>

# In[26]:

queryString = """
SELECT  ?p (COUNT(?s) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count
"""
results = performSparqlQuery(queryString)

for c in results:
    print (c['p']['value'])
    print (c['count']['value'])


# <b> 11.  table: property vs. total number of distinct subjects in triples using the property
# </b>

# In[28]:

queryString = """
SELECT  ?p (COUNT(DISTINCT ?s ) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count
"""
results = performSparqlQuery(queryString)

for c in results:
    print (c['p']['value'])
    print (c['count']['value'])


# <b> 12. table: property vs. total number of distinct objects in triples using the property
#  </b>

# In[29]:

queryString = """
SELECT  ?p (COUNT(DISTINCT ?o ) AS ?count ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?count
"""
results = performSparqlQuery(queryString)
for c in results:
    print (c['p']['value'])
    print (c['count']['value'])

