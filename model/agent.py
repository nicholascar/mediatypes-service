from flask import Response, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, XSD, Literal
from pyldapi import Renderer, View
import _conf as conf


class AgentRenderer(Renderer):
    def __init__(self, request, uri):
        views = {
            'foaf': View(
                'FOAF Properties View',
                'name and mbox or homepage of a foaf:Agent',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/turtle',
                namespace='http://test.linked.data.gov.au/def/mt#'
            )
        }
        super().__init__(
            request,
            uri,
            views,
            'foaf'
        )

    def render(self):
        if hasattr(self, 'vf_error'):
            return Response(self.vf_error, status=406, mimetype='text/plain')
        else:
            if self.view == 'alternates':
                return self._render_alternates_view()
            elif self.view == 'foaf':
                if self.format in Renderer.RDF_MIMETYPES:
                    rdf = self._get_instance_rdf()
                    if rdf is None:
                        return Response('No triples contain that URI as subject', status=404, mimetype='text/plain')
                    else:
                        return Response(rdf, mimetype=self.format)
                else:  # only the HTML format left
                    deets = self._get_instance_details()
                    print(deets)
                    if deets is None:
                        return Response('That URI yielded no data', status=404, mimetype='text/plain')
                    else:
                        return render_template(
                            'agent.html',
                            deets=deets
                        )

    def _get_instance_details(self):
        sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI, returnFormat=JSON)
        q = '''
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT *
            WHERE {{
                <{0[uri]}>  foaf:name ?name .
                OPTIONAL {{ <{0[uri]}> foaf:mbox|foaf:homepage ?u . }}
            }}
        '''.format({'uri': self.uri})
        sparql.setQuery(q)
        d = sparql.query().convert()
        d = d.get('results').get('bindings')
        if d is None or len(d) < 1:  # handle no result
            return None

        return {
            'name': str(d[0].get('name').get('value')),
            'u': str(d[0].get('u').get('value')) if str(d[0].get('u').get('value')) is not None else None
        }

    def _get_instance_rdf(self, rdf_format='turtle'):
        deets = self._get_instance_details()

        g = Graph()
        FOAF = Namespace('http://xmlns.com/foaf/0.1/')
        g.bind('foaf', FOAF)

        me = URIRef(self.uri)
        g.add((me, RDF.type, FOAF.Agent))
        g.add((me, FOAF.name, Literal(deets.get('name'), datatype=XSD.string)))
        if deets.get('u') is not None:
            g.add((me, RDFS.label, URIRef(deets.get('u'))))

        return g.serialize(format=rdf_format)
