from flask import Response, render_template
from rdflib import Graph, URIRef, RDF, XSD, OWL, Literal
from rdflib.namespace import DCTERMS
from pyldapi import Renderer, Profile
import model.sparql as s


class MediaTypeRenderer(Renderer):
    def __init__(self, request, instance_uri):
        views = {
            "mt": Profile(
                "https://w3id.org/profile/mediatype",
                "Mediatype Profile",
                "Basic properties of a Media Type, as recorded by IANA",
                ["text/html"] + Renderer.RDF_MEDIA_TYPES,
                "text/html",
                languages=["en", "pl"],
                default_language="en",
            )
        }
        super().__init__(request, instance_uri, views, "mt")

    def render(self):
        response = super().render()
        if response is None:
            if self.profile == "mt":
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
                            headers=self.headers,
                        )
                    else:
                        mediatype = (
                            self.instance_uri.replace("%2B", "+")
                            .replace("%2F", "/")
                            .split("/mediatype/")[1]
                        )
                        if self.language == "pl":
                            content = render_template(
                                "mediatype-pl.html", deets=deets, mediatype=mediatype
                            )
                        else:
                            content = render_template(
                                "mediatype-en.html", deets=deets, mediatype=mediatype
                            )

                        return Response(
                            content, mimetype=self.mediatype, headers=self.headers
                        )
        return response

    def _get_instance_details(self):
        q = """
            PREFIX dct:  <http://purl.org/dc/terms/>
            SELECT ?title ?contributor
            WHERE {{
                <{0[uri]}> dct:title ?title .
                OPTIONAL {{ <{0[uri]}> dct:contributor ?contributor . }}
            }}
        """.format(
            {"uri": self.instance_uri}
        )

        title = None
        contributors = []
        for r in s.sparql_query(q):
            title = str(r[0])
            contributors.append(str(r[1]))

        return None if title is None else {"title": title, "contributors": contributors}

    def _get_instance_rdf(self):
        deets = self._get_instance_details()

        g = Graph()
        g.bind("dct", DCTERMS)
        g.bind("owl", OWL)
        me = URIRef(self.instance_uri)
        g.add((me, RDF.type, DCTERMS.FileFormat))
        g.add(
            (
                me,
                OWL.sameAs,
                URIRef(
                    self.instance_uri.replace(
                        "https://w3id.org/mediatype/",
                        "https://www.iana.org/assignments/media-types/",
                    )
                ),
            )
        )
        g.add((me, DCTERMS.title, Literal(deets.get("title"), datatype=XSD.string)))
        source = (
            "https://www.iana.org/assignments/media-types/"
            + self.instance_uri.replace("%2B", "+")
            .replace("%2F", "/")
            .split("/mediatype/")[1]
        )
        g.add((me, DCTERMS.source, URIRef(source)))
        if deets.get("contributors") is not None:
            for contributor in deets.get("contributors"):
                g.add((me, DCTERMS.contributor, URIRef(contributor)))

        if self.mediatype in ["application/rdf+json", "application/json"]:
            return g.serialize(format="json-ld")
        else:
            return g.serialize(format=self.format)
