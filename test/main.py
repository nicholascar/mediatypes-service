import model.mediatype
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, N3, RDFXML
import _conf as conf
from rdflib import Graph, Namespace


# g = Graph().parse('../iana.ttl', format='turtle')
#
# uri = 'https://w3id.org/mediatype/application/3gpdash-qoe-report+xml'
# uri2 = 'https://w3id.org/mediatype/application/EmergencyCallData.Comment+xml'
#
# q = '''
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX dct:  <http://purl.org/dc/terms/>
#     SELECT *
#     WHERE {{
#         <{0[uri]}>  rdfs:label ?label .
#         OPTIONAL {{ <{0[uri]}> dct:contributor ?contributor . }}
#     }}
#     '''.format({'uri': uri2})
#
# contributors = []
# for r in g.query(q):
#     label = str(r['label'])
#     contributors.append(str(r['contributor']))
#
#
# print(label)
# print(contributors)


# def _get_instance_rdf(uri):
#     q = '''DESCRIBE <{0[uri]}>'''.format({'uri': uri})
#     return _sparql_query(q, RDFXML)


def query_turtle(sparql_query):
    import requests

    """Make a SPARQL query with turtle format response"""
    data = {'query': sparql_query, 'format': 'text/turtle'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    r = requests.post(conf.SPARQL_QUERY_URI, data=data, auth=auth, headers=headers, timeout=1)
    try:
        return r.content
    except Exception as e:
        raise


def instance_describe(uri, rdf_format):
    q = 'DESCRIBE <{}>'.format(uri)
    # convert the result from the SPARQL query to turtle and back to tidy it up for viewing
    triples = query_turtle(q)
    if len(triples) < 1 or triples is None:
        return None
    g = Graph().parse(data=triples.decode('utf-8'), format='turtle')

    g.bind('dct', Namespace('http://purl.org/dc/terms/'))

    if rdf_format in ['application/rdf+json', 'application/json']:
        return g.serialize(format='json-ld')
    else:
        return g.serialize(format=rdf_format)

print(instance_describe('https://w3id.org/mediatype/application/3gpdash-qoe-report+xmlzzz', 'turtle'))
#p#rint(_get_instance_rdf('https://w3id.org/mediatype/application/3gpdash-qoe-report+xml'))
