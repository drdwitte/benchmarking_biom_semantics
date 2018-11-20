/*
Copyright 2011-2014 Cray Inc. All Rights Reserved

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

* Neither the name Cray Inc. nor the names of its contributors may be
  used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
*/

package net.sf.sparql.benchmarking.operations.parameterized;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

import org.apache.jena.query.ParameterizedSparqlString;
import org.apache.jena.sparql.core.Var;
import org.apache.jena.sparql.engine.binding.Binding;

import net.sf.sparql.benchmarking.operations.AbstractOperation;

/**
 * Abstract parameterized SPARQL operation
 * 
 * @author rvesse
 * 
 */
public abstract class AbstractParameterizedSparqlOperation extends AbstractOperation {

    private ParameterizedSparqlString sparqlStr;
    private List<Binding> pool = new ArrayList<Binding>();
    private Random random = new Random();

    /**
     * Creates a new parameterized SPARQL operation
     * 
     * @param sparqlString
     *            SPARQL string
     * @param parameters
     *            Parameters to inject, each binding represents a single set of
     *            parameters
     * @param name
     *            Name
     */
    public AbstractParameterizedSparqlOperation(String sparqlString, Collection<Binding> parameters, String name) {
        super(name);
        this.sparqlStr = new ParameterizedSparqlString(sparqlString);
        this.pool.addAll(parameters);
    }

    /**
     * Gets the parameterized SPARQL with a random set of parameters injected
     * 
     * @return Parameterized SPARQL string
     */
    protected final ParameterizedSparqlString getParameterizedSparql() {
        this.sparqlStr.clearParams();
        int r = this.random.nextInt(this.pool.size());
        Binding b = this.pool.get(r);

        Iterator<Var> vs = b.vars();
        while (vs.hasNext()) {
            Var v = vs.next();
            this.sparqlStr.setParam(v.getName(), b.get(v));
        }

        return this.sparqlStr;
    }

    @Override
    public String getContentString() {
        StringBuilder builder = new StringBuilder();
        builder.append(sparqlStr.getCommandText());
        builder.append('\n');
        builder.append("Available Parameters (" + this.pool.size() + " sets):\n");
        for (Binding b : this.pool)
        {
            builder.append(b.toString() + "\n");
        }
        return builder.toString();
    }
}