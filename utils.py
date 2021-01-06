import urllib
import _config as config


def url_decode(s):
    try:
        return urllib.parse.unquote(s)
    except:
        pass


def url_encode(s):
    try:
        return urllib.parse.quote(s)
    except:
        pass


def get_system_uri(absolute_uri, system_uri_override):
    if system_uri_override is not None:
        return system_uri_override
    else:
        return "{}/object?uri={}".format(
            config.SYSTEM_URI_BASE, url_encode(absolute_uri)
        )


def get_absolute_uri(uri):
    if "uri=" in uri:
        uri = uri.split("uri=")[1]
    return url_decode(uri)


def get_content_uri(uri, system_uri_override=None):
    if config.USE_SYSTEM_URIS:
        return get_system_uri(uri, system_uri_override)
    else:
        return get_absolute_uri(uri)


def get_pretty_mediatype(mediatype):
    MEDIATYPE_NAMES = {
        "text/html": "HTML",
        "application/json": "JSON",
        "text/turtle": "Turtle",
        "application/rdf+xml": "RDF/XML",
        "application/ld+json": "JSON-LD",
        "text/n3": "Notation-3",
        "application/n-triples": "N-Triples",
    }
    return MEDIATYPE_NAMES.get(mediatype, mediatype)
