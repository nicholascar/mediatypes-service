from flask import Response, render_template
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, XSD, Literal
from pyldapi import Renderer, Profile
import model.sparql as s


class AgentRenderer(Renderer):
    def __init__(self, request, instance_uri):
        views = {
            "foaf": Profile(
                "http://xmlns.com/foaf/0.1/",
                "FOAF Properties Profile",
                "name and mbox or homepage of a foaf:Agent",
                ["text/html"] + Renderer.RDF_MEDIA_TYPES,
                "text/turtle",
                ["en"],
                "en",
            )
        }
        super().__init__(request, instance_uri, views, "foaf")

    def render(self):
        response = super().render()
        if response is None:
            if self.profile == "foaf":
                if self.mediatype in Renderer.RDF_MEDIA_TYPES:
                    rdf = self._get_instance_rdf()
                    if rdf is None:
                        return Response(
                            "No triples contain that URI as subject",
                            status=404,
                            mimetype="text/plain",
                        )
                    else:
                        return Response(
                            rdf, mimetype=self.mediatype, headers=self.headers
                        )
                else:  # only the HTML mediatype left
                    deets = self._get_instance_details()
                    if deets is None:
                        return Response(
                            "That URI yielded no data",
                            status=404,
                            mimetype="text/plain",
                        )
                    else:
                        content = render_template("agent.html", deets=deets)
                return Response(content, mimetype=self.mediatype, headers=self.headers)
        return response

    def _get_instance_details(self):
        # sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI, returnFormat=JSON)
        q = """
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
        """.format(
            {"uri": self.instance_uri}
        )

        name = None
        u = None
        mt = []
        for r in s.sparql_query(q):
            name = str(r[0])
            u = str(r[1])
            mt.append((str(r[2]), str(r[3])))

        return None if name is None else {"name": name, "u": u, "mt": mt}

    def _get_instance_rdf(self):
        deets = self._get_instance_details()

        g = Graph()
        FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        g.bind("foaf", FOAF)

        me = URIRef(self.instance_uri)
        g.add((me, RDF.type, FOAF.Agent))
        g.add((me, FOAF.name, Literal(deets.get("name"), datatype=XSD.string)))
        if deets.get("u") is not None:
            g.add((me, RDFS.label, URIRef(deets.get("u"))))

        if self.mediatype in ["application/rdf+json", "application/json"]:
            return g.serialize(format="json-ld")
        else:
            return g.serialize(format=self.format)
