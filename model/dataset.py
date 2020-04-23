from pyldapi import Renderer, Profile
import os
from flask import Response, render_template
from rdflib import Graph
import _conf as conf


class DatasetRenderer(Renderer):
    """
    Specialised implementation of the Renderer for displaying DCAT v2, VOID & Reg properties for the GNAF dataset as a
    whole. All content is contained in static HTML & RDT (turtle) files
    """

    def __init__(self, request, instance_uri):
        profiles = {
            "dcat": Profile(
                "https://www.w3.org/TR/vocab-dcat-2/",
                "Dataset Catalog Vocabulary - DCAT",
                "The DCAT view, according to DCATv2 (2018)",
                ["text/html"] + Renderer.RDF_MEDIA_TYPES,
                "text/html",
            ),
            "reg": Profile(
                "http://purl.org/linked-data/registry",
                "Registry Ontology view",
                "A 'core ontology for registry services': items are listed in Registers with acceptance statuses",
                ["text/html"] + Renderer.RDF_MEDIA_TYPES,
                "text/html",
            ),
            "void": Profile(
                "http://rdfs.org/ns/void",
                "Vocabulary of Interlinked Data Ontology view",
                "VoID is 'an RDF Schema vocabulary for expressing metadata about RDF datasets'",
                Renderer.RDF_MEDIA_TYPES,
                "text/turtle",
            ),
        }
        super().__init__(request, instance_uri, profiles, "dcat")

    def render(self):
        response = super().render()
        if response is None:
            if self.profile == "reg":
                if self.mediatype == "text/html":
                    return render_template("page_home_reg.html")
                else:
                    return self._render_rdf_from_file("reg.ttl", self.mediatype)
            elif self.profile == "void":
                # VoID view is only available in RDF
                return self._render_rdf_from_file("void.ttl", self.mediatype)
            else:  # elif self.profile == 'dcat':  # DCAT, default
                if self.mediatype == "text/html":
                    return Response(
                        render_template("page_home.html"),
                        mimetype=self.mediatype,
                        headers=self.headers,
                    )
                else:
                    return self._render_rdf_from_file("dcat.ttl", self.mediatype)
        return response

    def _render_rdf_from_file(self, file, mediatype):
        if self.mediatype == "text/turtle":
            txt = (
                open(os.path.join(conf.APP_DIR, "view", file), "rb")
                .read()
                .decode("utf-8")
            )
            return Response(txt, mimetype="text/turtle")
        else:
            g = Graph().parse(os.path.join(conf.APP_DIR, "view", file), format="turtle")
            if mediatype == "_internal":
                return g
            return Response(
                g.serialize(destination=None, format=format, encoding="utf-8"),
                mimetype=mediatype,
            )
