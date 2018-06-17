from SPARQLWrapper import SPARQLWrapper, JSON
import _conf as conf


def sparql_query(q):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results["results"]["bindings"]


def total_mediatypes():
    q = '''
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT (COUNT(*) as ?count) WHERE {?s a dct:FileFormat .}
    '''
    count = sparql_query(q)[0].get('count')
    if count is None:
        return None
    return int(count.get('value'))


def total_agents():
    q = '''
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (COUNT(*) as ?count) WHERE {?s a foaf:Agent .}
    '''
    count = sparql_query(q)[0].get('count')
    if count is None:
        return None
    return int(count.get('value'))
