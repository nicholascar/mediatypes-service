import requests
import conneg_headers


#
#   Test checking Content-Profile and Content-Type response headers
#
def test_conneg_p_defaults():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'Content-Profile is {}, should be default <https://w3id.org/profile/mediatype>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/html'), \
        'Content-Type is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# _format = 'text/turtle'
def test_conneg_p_accept_qsa_format_turtle():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={'_format': 'text/turtle'}
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'Content-Profile is {}, should be default <https://w3id.org/profile/mediatype>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/turtle'), \
        'Content-Type is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# _mediatype = 'text/turtle'
def test_conneg_p_accept_qsa_mediatype_turtle():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={'_mediatype': 'text/turtle'}
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'Content-Profile is {}, should be default <https://w3id.org/profile/mediatype>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/turtle'), \
        'Content-Type is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# _profile = 'mt'
# _mediatype = 'text/turtle'
def test_conneg_p_profile_qsa_mt_n3():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={
            '_profile': 'mt',
            '_mediatype': 'text/n3'
        }
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'Content-Profile is {}, should be <https://w3id.org/profile/mediatype>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/n3'), \
        'Content-Type is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# _profile = 'alternates'
# _mediatype = 'text/turtle'
def test_conneg_p_profile_qsa_alternates_turtle():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={
            '_profile': 'alternates',
            '_mediatype': 'text/turtle'
        }
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/alt>', \
        'Content-Profile is {}, should be <https://w3id.org/profile/alt>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/turtle'), \
        'Content-Profile is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# Accept-Profile: <https://w3id.org/profile/alt>
# Accept: 'text/turtle'
def test_conneg_p_profile_http_alternates_turtle():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        headers={
            'Accept-Profile': '<https://w3id.org/profile/alt>,'
                              '<https://w3id.org/profile/other>;q=0.5,'
                              '<https://w3id.org/profile/other,comma>;q=0.5,'
                              '<urn:example:profile:x>;q=0.6,'
                              '<urn:example:profile:y,comma;semicolon>;q=0.7',
            'Accept': 'text/turtle'
        }
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/alt>', \
        'Content-Profile is {}, should be <https://w3id.org/profile/alt>'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/turtle'), \
        'Content-Profile is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


# Accept-Profile: <https://w3id.org/profile/none>  # non-existent profile therefor default, i.e. mt
# Accept: 'text/turtle'
def test_conneg_p_profile_http_none_turtle():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        headers={
            'Accept-Profile': '<https://w3id.org/profile/none>',
            'Accept': 'text/turtle'
        }
    )
    # check the HTTP headers
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'Content-Profile is {}, should be default https://w3id.org/profile/mediatype'.format(r.headers.get('Content-Profile'))

    assert r.headers.get('Content-Type').startswith('text/turtle'), \
        'Content-Profile is {}, should be text/turtle'.format(r.headers.get('Content-Type'))


#
#   Test checking Conneg by P Link response headers
#
# defaults ('https://w3id.org/profile/mediatype' & 'text/turtle)
def test_conneg_link_header_default():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/mediatype', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/mediatype'.format(this_profile)


# Accept-Profile: <https://w3id.org/profile/alt>
def test_conneg_link_header_alternates():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        headers={'Accept-Profile': '<https://w3id.org/profile/alt>'}
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/alt', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/alt'.format(this_profile)


# Accept-Profile: <https://w3id.org/profile/alt>
# Accept: application/ld+json
def test_conneg_link_header_alternates_json_ld():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        headers={
            'Accept-Profile': '<https://w3id.org/profile/alt>',
            'Accept': 'application/ld+json'
        }
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/alt', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/alt'.format(this_profile)
            this_type = l.split('type="')[1].split('"')[0]
            assert this_type == 'application/ld+json', \
                'The type="" was {}, should be application/ld+json'.format(this_type)


# _profile=https://w3id.org/profile/alt
# AND
# Accept-Profile: <https://w3id.org/profile/mediatype>
def test_conneg_profile_collision_1():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={'_profile': '<https://w3id.org/profile/mediatype>'},
        headers={'Accept-Profile': '<https://w3id.org/profile/alt>'}
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/mediatype', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/mediatype'.format(this_profile)


# _profile=https://w3id.org/profile/mediatype
# AND
# Accept-Profile: <https://w3id.org/profile/alt>
def test_conneg_profile_collision_2():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={'_profile': '<https://w3id.org/profile/alt>'},
        headers={'Accept-Profile': '<https://w3id.org/profile/mediatype>'}
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/alt', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/alt'.format(this_profile)


# _profile=http://test.linked.data.gov.au/def/xxx# - not a valid profile
# AND
# Accept-Profile: <https://w3id.org/profile/alt>
def test_conneg_profile_collision_3():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri,
        params={'_profile': '<http://test.linked.data.gov.au/def/xxx#>'},
        headers={'Accept-Profile': '<https://w3id.org/profile/alt>'}
    )
    # check the Link headers
    link_header = r.headers.get('Link').lstrip('Link: ').split(',')
    for l in link_header:
        if 'rel="self"' in l:
            this_profile = l.split('profile="')[1].rstrip('"')
            assert this_profile == 'https://w3id.org/profile/mediatype', \
                'The rel="self" profile="" was {}, should have been https://w3id.org/profile/mediatype'.format(this_profile)


# Abstract Model
#
# List Profiles
#
# HTTP:
#   Request:    any resource URI, no headers
#   Response:   Link header
def list_profiles_http():
    uri = 'http://localhost:5000/object?uri=https://w3id.org/mediatype/text/n3'
    r = requests.get(
        uri
    )

    # check that the Content-Profile header exists and that it's the default profile
    assert r.headers.get('Content-Profile') == '<https://w3id.org/profile/mediatype>', \
        'default Content-Profile is {}'.format(r.headers.get('Content-Profile'))

    # check that the Link header exists
    assert r.headers.get('Link') is not None, 'Link header is missing'

    # check that the Link header is valid for list profiles
    lh = conneg_headers.LinkHeaderParser(r.headers.get('Link'))
    assert lh.valid_list_profiles


# QSA:
#   Request:    uri?_profile=all
#   Response:   Link header
def list_profiles_qsa(uri):
    r = requests.get(
        uri,
        params={'_profile': 'all'}
    )

    # check that the Link header exists
    assert r.headers.get('Link') is not None, 'Link header is missing'

    # check that the Link header is valid for list profiles
    lh = conneg_headers.LinkHeaderParser(r.headers.get('Link'))
    lp_check = lh.is_valid_list_profiles()
    assert lp_check[0], lp_check[1]


# QSA Alternates:
#   Request:    uri?_view=alternates
#   Response:   Link header
def list_profiles_qsa_alternate(uri):
    r = requests.get(
        uri,
        params={'_view': 'alternates'}
    )

    # check that the Link header exists
    assert r.headers.get('Link') is not None, 'Link header is missing'

    # check that the Link header is valid for list profiles
    lh = conneg_headers.LinkHeaderParser(r.headers.get('Link'))
    lp_check = lh.is_valid_list_profiles()
    assert lp_check[0], lp_check[1]


if __name__ == '__main__':

    test_conneg_p_defaults()
    test_conneg_p_accept_qsa_format_turtle()
    test_conneg_p_accept_qsa_mediatype_turtle()
    test_conneg_p_profile_qsa_mt_n3()
    test_conneg_p_profile_qsa_alternates_turtle()
    test_conneg_p_profile_http_alternates_turtle()
    test_conneg_p_profile_http_none_turtle()

    test_conneg_link_header_default()
    test_conneg_link_header_alternates()
    test_conneg_link_header_alternates_json_ld()

    test_conneg_profile_collision_1()
    test_conneg_profile_collision_2()
    test_conneg_profile_collision_3()

    list_profiles_http()
    # list_profiles_qsa()
    # list_profiles_qsa_alternate()
