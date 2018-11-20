GREEN='\033[0;32m'
RED='\033[0;31m'
NO_COLOUR='\033[0m'
DELIMITER="****************************************************************************************************\n* "

printf "${GREEN}${DELIMITER}Deleting repository${NO_COLOUR}\n\n"

curl -X POST -H "Content-Type:application/x-www-form-urlencoded" --data-urlencode "update=DELETE WHERE { GRAPH <http://example.com> { ?s ?p ?o}}"  http://localhost:8080/repositories/SYSTEM/statements

printf "${GREEN}${DELIMITER}Creating repository in SYSTEM${NO_COLOUR}\n\n"

curl -X POST -H "Content-Type:application/x-turtle" -T repository-config.ttl http://localhost:8080/repositories/SYSTEM/rdf-graphs/service?graph=http://example.com#g1

printf "${GREEN}${DELIMITER}Resgitrating the repository${NO_COLOUR}\n\n"

curl -X POST -H "Content-Type:application/x-turtle" -d "<http://example.com#g1> a <http://www.openrdf.org/config/repository#RepositoryContext>." http://localhost:8080/repositories/SYSTEM/statements

