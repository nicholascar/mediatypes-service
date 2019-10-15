from pyldapi import Renderer, View
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
        views = {
            'dcat': View(
                'Dataset Catalog Vocabulary - DCAT',
                'The DCAT view, according to DCATv2 (2018)',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/html',
                profile_uri='http://www.w3.org/ns/dcat'
            ),
            'reg': View(
                'Registry Ontology view',
                'A \'core ontology for registry services\': items are listed in Registers with acceptance statuses',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/html',
                profile_uri='http://purl.org/linked-data/registry'
            ),
            'void': View(
                'Vocabulary of Interlinked Data Ontology view',
                'VoID is \'an RDF Schema vocabulary for expressing metadata about RDF datasets\'',
                Renderer.RDF_MIMETYPES,
                'text/turtle',
                profile_uri='http://rdfs.org/ns/void'
            ),
        }
        super().__init__(
            request,
            instance_uri,
            views,
            'dcat'
        )

    def render(self):
        response = super().render()
        if response is None:
            if self.view == 'reg':
                if self.format == 'text/html':
                    return render_template('page_home_reg.html')
                else:
                    return self._render_rdf_from_file('reg.ttl', self.format)
            elif self.view == 'void':
                # VoID view is only available in RDF
                return self._render_rdf_from_file('void.ttl', self.format)
            else:  # elif self.view == 'dcat':  # DCAT, default
                if self.format == 'text/html':
                    return Response(render_template('page_home.html'), mimetype=self.format, headers=self.headers)
                else:
                    return self._render_rdf_from_file('dcat.ttl', self.format)
        return response

    def _render_rdf_from_file(self, file, format):
        if self.format == 'text/turtle':
            txt = open(os.path.join(conf.APP_DIR, 'view', file), 'rb').read().decode('utf-8')
            return Response(txt, mimetype='text/turtle')
        else:
            g = Graph().parse(os.path.join(conf.APP_DIR, 'view', file), format='turtle')
            if format == "_internal":
                return g
            return Response(
                g.serialize(destination=None, format=format, encoding='utf-8'),
                mimetype=format
            )
