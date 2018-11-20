# Mail support (Andreas Schwarte)

### drdwitte@gmail.com (september 5, 2016)

Dear Andreas,

My name is Dieter De Witte, I work together with Laurens De Vocht on a project with Ontoforce where we are studying sparql query federation. I'll quickly sketch the contours of what we are trying to accomplish.

I'd like to test two setups. N=1 and N=3 nodes setup on Amazon Webservices. These nodes will run a Virtuoso Sparql server. I have a set of queries which I want to run (automated via HTTP requests. How? We'd like to use your workbench software as a SPARQL endpoint and define 1 or 3 sources of federation. I have some small questions:

1) Security: I'd like to disable security as much as possible, but I am a bit lost in the security parameters in the workbench, is it possible to give me some pointers. Preferable I'd like to query a sparql endpoint as for example http://<ip>:<port>/sparql

2) I tested the UI and it's possible to query the remote resources if I mark them as federated and then in /sparql UI, select federated as the repository. Now, if I want to automate this, is federated automatically selected if I query the endpoint or do I need to provide an extra parameter specifying the repository against which to query?

Thanks a lot for your input, we are very interested in the results of FluidOps.

Kind Regards,
Dieter De Witte
iMinds - Data Science Lab
Ghent University

### andreas.schwarte@fluidops.com (september 6, 2016)

Dear Dieter,

thanks for following up on this.

Regarding your questions:

1) You can open the SPARQL endpoint for non-authenticated by putting a file "role-publicSparqlEndpoint.acl" into the "config/acl/extensions/" folder of your installation

`### Extension role ###`

`@includeRole: sparql-query`

`@includedByRole: guest`

This means that each "guest" user (i.e. including non-authenticated users) also have access to perform SPARQL queries in the SPARQL endpoint.

Note: if you do not want to restart Information Workbench, you can reload the ACL definitions on the /resource/Admin:Permissions page. A second hint: when you are using authenticated users, one would rather use role-mappings than this extension mechanism.

If you want to enable http you can search for the "enableHttp" setting on the system configuration page "resource/Admin:Config" and set the value to true. Note that this requires a restart


2) To access one of the managed repositories you can use the request parameter "repository=<repositoryid>", e.g.in your case  "/sparql?repository=federated"


Some more hints for you:

* for Virtuoso we offer an app that provides a bridge/connector to the triple store. This connector uses an optimized protocol (i.e. it does not access the virtuoso SPARQL endpoint directly). See https://appcenter.fluidops.com/resource/?uri=http%3A%2F%2Fwww.fluidops.com%2Fapplication%2Fvirtuoso-bridge

* Using the SPARQL 1.1 federation extensions you can easily access all repositories managed by Information Workbench by their ID. When designing and building applications (i.e. UIs) this might sometimes be more suitable than using a complete federation layer. You can achieve this via "SERVICE System:myrepositoryid { ....}" inside a query.

* If you have not already done so, I would suggest you to try out the visualization widgets of Information Workbench and how easy it is to build UIs (e.g. by defining a simple wiki template for a concept). This directly allows browsing all the data.


One more hint: if you have further questions that are of general interest, I would like to ask you to direct your questions to our community discussions mailing list: iwb-discussion@googlegroups.com

Best,
 Andreas

### drdwitte@gmail.com (september 6, 2016)

Dear Andreas,

Just a very small follow-up question.

"/sparql?repository=federated"

Is it possible to have the default repository be federated, so I don't need to provide the extra repo parameter? The benchmarker software we use for testing only allows a sparql endpoint to be set and no additional parameters as far as I see.

Kind Regards,
Dieter De Witte

### andreas.schwarte@fluidops.com (september 7, 2016)



Dear Dieter,

yes, this is possible, but I would only recommend to do such configuration for evaluation / testing purposes. For production use-cases or actual applications it is preferred to go with the repository configuration inside widgets.

See http://help.fluidops.com/resource/Help:RepositoryConfiguration#Federation_with_FedX for the details of the configuration.

Best,
 Andreas
