import _conf as conf


def sparql_query(q):
    # sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI)
    # sparql.setQuery(q)
    # sparql.setReturnFormat(JSON)
    # results = sparql.query().convert()
    #
    # return results["results"]["bindings"]

    r = conf.G.query(q)
    return r


def total_mediatypes():
    q = '''
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT (COUNT(*) as ?count) WHERE {?s a dct:FileFormat .}
    '''
    count = None
    for r in sparql_query(q):
        count = r[0]
    return int(count) if count is not None else None


def total_agents():
    q = '''
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (COUNT(*) as ?count) WHERE {?s a foaf:Agent .}
    '''
    count = None
    for r in sparql_query(q):
        count = r[0]
    return int(count) if count is not None else None
