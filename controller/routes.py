from flask import Blueprint, request, redirect, url_for, render_template, Response
from pyldapi import ContainerRenderer
from model.mediatype import MediaTypeRenderer
from model.agent import AgentRenderer
from model.dataset import DatasetRenderer
from model import sparql as s
import os
import _config as conf
import utils as u

routes = Blueprint("controller", __name__)


@routes.context_processor
def context_processor():
    """
    A set of variables available globally for all Jinja templates.
    :return: A dictionary of variables
    :rtype: dict
    """
    return dict(utils=u,)  # gives access to all functions defined in utils.py


#
#   pages
#
@routes.route("/")
def home():
    return DatasetRenderer(request, request.base_url).render()


@routes.route("/about")
def about():
    return render_template("page_home.html")


@routes.route("/connegp")
def connegp():
    return render_template("connegp.html")


#
#   registers
#
@routes.route("/reg/")
def reg():
    return redirect(url_for("controller.home") + "?_profile=reg")


@routes.route("/mediatype/")
def mediatypes():
    per_page = request.args.get("per_page", type=int, default=20)
    page = request.args.get("page", type=int, default=1)

    total = s.total_mediatypes()
    if total is None:
        return Response("_data store is unreachable", status=500, mimetype="text/plain")

    # get list of org URIs and labels from the triplestore
    q = """
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?uri ?title
        WHERE {{
            ?uri a dct:FileFormat ;
                 dct:title ?title .
        }}
        ORDER BY ?title
        LIMIT {}
        OFFSET {}
    """.format(
        per_page, (page - 1) * per_page
    )

    register = []
    for r in s.sparql_query(q):
        register.append((url_for("controller.object") + "?uri=" + str(r[0]), str(r[1])))

    return ContainerRenderer(
        request,
        "https://mediatypes.conneg.info/mediatype/",
        "Register of Media Types",
        "All the Media Types in IANA's list at <code>https://www.iana.org/assignments/media-types/media-types.xml.</code>",
        "https://mediatypes.conneg.info/reg/",
        "MediaTypes Service",
        register,
        total,
    ).render()


@routes.route("/mediatype/agent/")
def agents():
    per_page = request.args.get("per_page", type=int, default=20)
    page = request.args.get("page", type=int, default=1)

    total = s.total_mediatypes()
    if total is None:
        return Response("_data store is unreachable", status=500, mimetype="text/plain")

    # get list of org URIs and labels from the triplestore
    q = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?uri ?name
        WHERE {{
            ?uri a foaf:Agent ;
                 foaf:name ?name .
        }}
        ORDER BY ?name
    """.format(
        per_page, (page - 1) * per_page
    )

    register = []
    for r in s.sparql_query(q):
        register.append((str(r[0]), str(r[1])))

    return ContainerRenderer(
        request,
        "http://localhost:5000/person/",
        "Register of Agents",
        "People and Organizations who have registered Media Types",
        "http://localhost:5000/reg/",
        "MediaTypes Service",
        register,
        total,
    ).render()


#
#   instances
#
@routes.route("/object")
def object():
    if request.args.get("uri") is not None and str(request.args.get("uri")).startswith(
        "http"
    ):
        uri = request.args.get("uri")
    else:
        return Response(
            "You must supply the URI if a resource with ?uri=...",
            status=400,
            mimetype="text/plain",
        )
    # protecting against '+' being rendered as a space in MTs like application/rdf+xml
    uri = uri.replace(" ", "+")

    # distinguish Media Types from Agents
    if "/agent/" in uri:
        return AgentRenderer(request, uri).render()
    else:
        return MediaTypeRenderer(request, uri).render()


# mediatype alias
@routes.route("/mediatype/<path:mt>")
def mediatype_redirect(mt):
    return redirect(
        url_for("controller.object", uri="https://w3id.org/mediatype/" + mt)
    )


@routes.route("/mediatypes.ttl")
def mediatypes_ttl():
    return Response(
        open(os.path.join(conf.APP_DIR, "mediatypes.ttl"), "rb").read(),
        mimetype="text/turtle",
    )


@routes.route("/mediatypes.tar.gz")
def mediatypes_gzip():
    return Response(
        open(os.path.join(conf.APP_DIR, "mediatypes.tar.gz"), "rb").read(),
        mimetype="application/gzip",
    )
