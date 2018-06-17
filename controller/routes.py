from flask import Blueprint, request
from pyldapi import *
from model.mediatype import MediaTypeRenderer
from model.agent import AgentRenderer
from model import sparql
import _conf as conf

routes = Blueprint('controller', __name__)


@routes.route('/')
def home():
    return render_template('page_home.html')


@routes.route('/reg/')
def reg():
    return RegisterOfRegistersRenderer(
        request,
        'http://localhost:5000/',
        'Register of Registers',
        'The master register of this API',
        conf.APP_DIR + '/rofr.ttl'
    ).render()


@routes.route('/mediatype/')
def mediatypes():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_mediatypes()
    if total is None:
        return Response('_data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Boards')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?uri ?label
        WHERE {{
            ?uri a dct:FileFormat ;
                 rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    mediatypes = sparql.sparql_query(q)

    for mediatype in mediatypes:
        o = str(mediatype['uri']['value'])
        l = str(mediatype['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/policy/',
        'Register of Media Types',
        'All the Media Types in IANA\'s list at https://www.iana.org/assignments/media-types/media-types.xml.',
        register,
        ['http://purl.org/dc/terms/FileFormat'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/agent/')
def agents():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_mediatypes()
    if total is None:
        return Response('_data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Boards')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?uri ?label
        WHERE {{
            ?uri a foaf:Agent ;
                 foaf:name ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    agents = sparql.sparql_query(q)

    for agent in agents:
        o = str(agent['uri']['value'])
        l = str(agent['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/policy/',
        'Register of Agents',
        'People and Organizations who have registered Media Type',
        register,
        ['http://xmlns.com/foaf/0.1/Agent'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/object')
def object():
    if request.args.get('uri') is not None and str(request.args.get('uri')).startswith('http'):
        uri = request.args.get('uri')
    else:
        return Response('You must supply the URI if a resource with ?uri=...', status=400, mimetype='text/plain')

    # distinguish Media Types from Agents
    if '/' in uri.replace('https://w3id.org/mediatype/', ''):
        return MediaTypeRenderer(request, uri).render()
    else:
        return AgentRenderer(request, uri).render()
