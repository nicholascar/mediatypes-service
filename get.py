import requests
from lxml import objectify
from rdflib import ConjunctiveGraph, URIRef, Literal, XSD, RDF, RDFS, Namespace
from rdflib.namespace import DCTERMS


# r = requests.get('https://www.iana.org/assignments/media-types/media-types.xml', headers={'Accept': 'text/xml'})
# with open('mediatypes.xml', 'w') as f:
#     f.write(r.text)

g = ConjunctiveGraph()
MT = Namespace('https://w3id.org/mediatype/')
g.bind('mt', MT)
g.bind('dct', DCTERMS)
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
g.bind('foaf', FOAF)

for register in objectify.parse('mediatypes.xml').getroot().getchildren():
    if register.tag == '{http://www.iana.org/assignments}registry':
        c = register.getchildren()
        category = c[0]
        for record in c:
            if record.tag == '{http://www.iana.org/assignments}record':
                if hasattr(record, 'file'):
                    me = URIRef(MT + record.file)
                    g.add((me, RDF.type, DCTERMS.FileFormat))
                    g.add((me, DCTERMS.title, Literal(record.name, datatype=XSD.string)))
                    for x in record.xref:
                        if x.get('data') is not None:
                            if x.get('type') == 'rfc':
                                g.add((me, DCTERMS.source, URIRef('https://tools.ietf.org/html/' + x.get('data'))))
                            elif x.get('type') == 'person':
                                g.add((me, DCTERMS.contributor, URIRef(MT + x.get('data'))))
    elif register.tag == '{http://www.iana.org/assignments}people':
        for person in register.getchildren():
            me = URIRef(MT + person.get('id'))
            g.add((me, RDF.type, FOAF.Agent))
            g.add((me, FOAF.name, Literal(person.name, datatype=XSD.string)))
            if hasattr(person, 'uri'):
                if str(person.uri).startswith('mailto:'):
                    g.get_context(URIRef(MT + 'person/')).add((
                        me,
                        FOAF.mbox,
                        URIRef(str(person.uri).replace('&', '@').replace(' at ', '@'))
                    ))
                else:  # normal URI, not email
                    g.get_context(URIRef(MT + 'person/')).add((
                        me,
                        FOAF.homepage,
                        URIRef(person.uri)
                    ))

with open('mediatypes.ttl', 'w') as f:
    f.write(g.serialize(format='turtle').decode('utf-8'))

