import requests
import connegp


# Dataset
def test_homepage():
    r = requests.get("http://localhost:5000")
    assert (
        "<title>Media Types Dataset</title>" in r.text
    ), "Homepage does not include <title>Media Types</title>"


def test_mediatypes_dataset_defaults():
    r = requests.get("http://localhost:5000")
    assert (
        '<h1 title="dct:title" class="rdf">Media Types Dataset</h1>' in r.text
    ), 'Homepage does not include <h1 title="dct:title" class="rdf">Media Types Dataset</h1>'


def test_mediatypes_dataset_reg_qsa():
    r = requests.get("http://localhost:5000", params={"_profile": "reg"})
    assert (
        "<h1>Media Types Register of Registers</h1>" in r.text
    ), "Homepage 'reg' view in HTML does not include <h1>Media Types Register of Registers</h1>"


def test_mediatypes_dataset_reg_http():
    r = requests.get(
        "http://localhost:5000",
        headers={"Accept-Profile": "<http://purl.org/linked-data/registry>"},
    )
    assert (
        "<h1>Media Types Register of Registers</h1>" in r.text
    ), "Homepage 'reg' view in HTML does not include <h1>Media Types Register of Registers</h1>"


# Register
def test_mediatypes_register_defaults():
    r = requests.get("http://localhost:5000/mediatype/")
    assert r.headers["Content-Profile"] == "<http://purl.org/linked-data/registry>", (
        "Media Types Register does not have a Content-Profile header of <http://purl.org/linked-data/registry>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/html"
    ), "Media Types Register does not have a header of Content-Type text/html, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        "<h1>Register</h1>" in r.text
    ), "Media Types Register does not include <h1>Register</h1>"


def test_mediatypes_register_reg_ttl_http():
    r = requests.get(
        "http://localhost:5000/mediatype/", headers={"Accept": "text/turtle"}
    )
    assert r.headers["Content-Profile"] == "<http://purl.org/linked-data/registry>", (
        "Media Types Register does not have a Content-Profile header of <http://purl.org/linked-data/registry>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Register of Media Types"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Register of Media Types"^^xsd:string ;'


def test_mediatypes_register_reg_ttl_qsa():
    r = requests.get(
        "http://localhost:5000/mediatype/", params={"_mediatype": "text/turtle"}
    )
    assert r.headers["Content-Profile"] == "<http://purl.org/linked-data/registry>", (
        "Media Types Register does not have a Content-Profile header of <http://purl.org/linked-data/registry>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Register of Media Types"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Register of Media Types"^^xsd:string ;'


def test_mediatypes_register_alternates_html_http():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        headers={"Accept-Profile": "<https://w3id.org/profile/alternates>"},
    )
    assert r.headers["Content-Profile"] == "<https://w3id.org/profile/alternates>", (
        "Media Types Register does not have a Content-Profile header of <https://w3id.org/profile/alternates>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/html"
    ), "Media Types Register does not have a header of Content-Type: text/html, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        "<h1>Alternates Profile</h1>" in r.text
    ), "Media Types Register does not include <h1>Register</h1>"


def test_mediatypes_register_alternates_ttl_http():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        headers={
            "Accept-Profile": "<https://w3id.org/profile/alternates>",
            "Accept": "text/turtle",
        },
    )
    assert r.headers["Content-Profile"] == "<https://w3id.org/profile/alternates>", (
        "Media Types Register does not have a Content-Profile header of <https://w3id.org/profile/alternates>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type: text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Alternates"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Alternates"^^xsd:string ;'


def test_mediatypes_register_alternates_ttl_qsa_token():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        params={"_profile": "alternates", "_mediatype": "text/turtle"},
    )
    assert r.headers["Content-Profile"] == "<https://w3id.org/profile/alternates>", (
        "Media Types Register does not have a Content-Profile header of <https://w3id.org/profile/alternates>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type: text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Alternates"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Alternates"^^xsd:string ;'


def test_mediatypes_register_alternates_ttl_qsa_uri():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        params={
            "_profile": "<https://w3id.org/profile/alternates>",
            "_mediatype": "text/turtle",
        },
    )
    assert r.headers["Content-Profile"] == "<https://w3id.org/profile/alternates>", (
        "Media Types Register does not have a Content-Profile header of <https://w3id.org/profile/alternates>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type: text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Alternates"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Alternates"^^xsd:string ;'


def test_mediatypes_register_alternates_ttl_qsa_alternate_keywords():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        params={
            "_view": "<https://w3id.org/profile/alternates>",
            "_format": "text/turtle",
        },
    )
    assert r.headers["Content-Profile"] == "<https://w3id.org/profile/alternates>", (
        "Media Types Register does not have a Content-Profile header of <https://w3id.org/profile/alternates>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type: text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Alternates"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Alternates"^^xsd:string ;'


def test_mediatypes_register_alternates_qsa_alternate_keywords_multi_profile():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        params={
            "_view": "<https://w3id.org/profile/alternates>;q=0.5,reg",  # i.e. reg;q=1
            "_format": "text/turtle",
        },
    )
    assert r.headers["Content-Profile"] == "<http://purl.org/linked-data/registry>", (
        "Media Types Register does not have a Content-Profile header of <http://purl.org/linked-data/registry>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/turtle"
    ), "Media Types Register does not have a header of Content-Type: text/turtle, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        'rdfs:label "Register of Media Types"^^xsd:string ;' in r.text
    ), 'Media Types Register does not include rdfs:label "Register of Media Types"^^xsd:string ;'


def test_mediatypes_register_reg_ttl_http_multi_profile():
    r = requests.get(
        "http://localhost:5000/mediatype/",
        headers={
            "Accept-Profile": "<https://w3id.org/profile/alternates>;q=0,<http://purl.org/linked-data/registry>,<http://example.org/profile/x>;q=0.8"
        },
    )
    assert r.headers["Content-Profile"] == "<http://purl.org/linked-data/registry>", (
        "Media Types Register does not have a Content-Profile header of <http://purl.org/linked-data/registry>, "
        "instead {}".format(r.headers["Content-Profile"])
    )
    assert r.headers["Content-Type"].startswith(
        "text/html"
    ), "Media Types Register does not have a header of Content-Type text/html, instead {}".format(
        r.headers["Content-Type"]
    )
    assert (
        "<h1>Register</h1>" in r.text
    ), "Media Types Register does not include <h1>Register</h1>"


def test_mediatypes_register_link_header_profiles_tokens():
    r = requests.get("http://localhost:5000/mediatype/")
    lh = connegp.LinkHeaderParser(r.headers["Link"])
    returned_profiles = []
    for profile in lh.profiles:
        returned_profiles.append(profile)

    returned_profiles = set(returned_profiles)
    expected_profiles = {
        "<https://w3id.org/profile/alternates>",
        "<http://purl.org/linked-data/registry>",
    }
    assert (
        returned_profiles == expected_profiles
    ), "Returned profiles should be {} but were {}".format(
        returned_profiles, expected_profiles
    )


# Instance - Media Type
def test_link_header_self_mediatype():
    r = requests.get(
        "http://localhost:5000/object",
        params={"uri": "https://w3id.org/mediatype/text/n3"},
    )

    lh = connegp.LinkHeaderParser(r.headers["Link"])

    for l in lh.link_headers:
        if l.get("rel") == "self":
            uri = l.get("uri")
            type = l.get("type")
            profile = l.get("profile")

    expected_header = {
        "uri": "https://w3id.org/mediatype/text/n3?_view=mt",
        "rel": "self",
        "type": "text/html",
        "profile": "https://w3id.org/profile/mediatype",
    }

    assert (
        uri == expected_header["uri"]
        and type == expected_header["type"]
        and profile == expected_header["profile"]
    ), "The 'self' URI in the Link header was {} {} {}, should have been {} {} {}.".format(
        uri,
        type,
        profile,
        expected_header["uri"],
        expected_header["type"],
        expected_header["profile"],
    )


if __name__ == "__main__":
    # test_homepage()
    test_mediatypes_dataset_defaults()
    test_mediatypes_dataset_reg_qsa()
    test_mediatypes_dataset_reg_http()
    # test_mediatypes_register_defaults()
    # test_mediatypes_register_reg_ttl_http()
    # test_mediatypes_register_reg_ttl_qsa()
    # test_mediatypes_register_alternates_html_http()
    # test_mediatypes_register_alternates_ttl_http()
    # test_mediatypes_register_alternates_ttl_qsa_token()
    # test_mediatypes_register_alternates_ttl_qsa_uri()
    # test_mediatypes_register_alternates_ttl_qsa_alternate_keywords()
    # test_mediatypes_register_alternates_qsa_alternate_keywords_multi_profile()
    # test_mediatypes_register_reg_ttl_http_multi_profile()
    # test_link_header_profiles_tokens()
    test_link_header_self()
