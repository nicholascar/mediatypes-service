from flask import Response, render_template
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, XSD, Literal
from pyldapi import Renderer, View
import model.sparql as s


class AgentRenderer(Renderer):
    def __init__(self, request, instance_uri):
        views = {
            'foaf': View(
                'FOAF Properties View',
                'name and mbox or homepage of a foaf:Agent',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/turtle',
                profile_uri='http://xmlns.com/foaf/0.1/'
            )
        }
        super().__init__(
            request,
            instance_uri,
            views,
            'foaf'
        )

    def render(self):
        response = super().render()
        if response is None:
            if self.view == 'foaf':
                if self.format in Renderer.RDF_MIMETYPES:
                    rdf = self._get_instance_rdf()
                    if rdf is None:
                        return Response('No triples contain that URI as subject', status=404, mimetype='text/plain')
                    else:
                        return Response(rdf, mimetype=self.format)
                else:  # only the HTML format left
                    deets = self._get_instance_details()
                    if deets is None:
                        return Response('That URI yielded no data', status=404, mimetype='text/plain')
                    else:
                        return render_template(
                            'agent.html',
                            deets=deets
                        )

    def _get_instance_details(self):
        # sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI, returnFormat=JSON)
        q = '''
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?name ?u ?mt ?title
            WHERE {{
                <{0[uri]}> foaf:name ?name .
                OPTIONAL {{ <{0[uri]}> foaf:mbox|foaf:homepage ?u . }}
                ?mt dct:contributor <{0[uri]}> ;
                    dct:title ?title .
            }}
            ORDER BY ?title
        '''.format({'uri': self.instance_uri})

        name = None
        u = None
        mt = []
        for r in s.sparql_query(q):
            name = str(r[0])
            u = str(r[1])
            mt.append((str(r[2]), str(r[3])))

        return None if name is None else {'name': name, 'u': u, 'mt': mt}

    def _get_instance_rdf(self, rdf_format='turtle'):
        deets = self._get_instance_details()

        g = Graph()
        FOAF = Namespace('http://xmlns.com/foaf/0.1/')
        g.bind('foaf', FOAF)

        me = URIRef(self.instance_uri)
        g.add((me, RDF.type, FOAF.Agent))
        g.add((me, FOAF.name, Literal(deets.get('name'), datatype=XSD.string)))
        if deets.get('u') is not None:
            g.add((me, RDFS.label, URIRef(deets.get('u'))))

        return g.serialize(format=rdf_format)
