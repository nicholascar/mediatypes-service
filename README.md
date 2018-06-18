<h1>Media Types Register</h1>
<p>This is a small API that re-presents Media Types in forms useful for Linked Data applications.</p>

<p>Media Types (used to be called MIME types, sometimes called <em>formats</em>, also see <a href="https://en.wikipedia.org/wiki/Media_type">Wikipedia</a>) are listed by <a href="https://www.iana.org/">IANA</a> at <a href="https://www.iana.org/assignments/media-types/media-types.xml">https://www.iana.org/assignments/media-types/media-types.xml</a> and we just take that data, convert it to <a href="https://www.w3.org/2001/sw/wiki/RDF">RDF</a>, store it, and serve it up using a small Python Linked Data API imaginatively called <a href="https://pypi.org/project/pyldapi/">pyLDAPI</a>.</p>
<h2>W3ID</h2>
<p><a href="https://w3id.org">W3ID</a> provides a "secure, permanent URL re-direction service for Web applications.</p>
<p>By using W3ID-based identifiers for each Media Type, this Register provides a stable way to refer to each Media Types by <a href="https://en.wikipedia.org/wiki/Uniform_Resource_Identifier">URI</a>.</p>

<p>This is not new or groundbreaking stuff but previous attempts to make this information available via URI seem to be offline (e.g. see <a href="http://purl.org/NET/mediatypes/">http://purl.org/NET/mediatypes/</a>).</p>

<h2>URIs &amp; RDF</h2>
<p>The initial reason for doing this is to allow the <a href="http://www.dublincore.org/documents/dcmi-terms/#terms-format">Dublin Core Terms property <em>format</em></a> to refer to stable, dereferenceable, URIs for Media Types rather than to made up ones or text strings.</p>

<p>For every MIME type in IANA's list, this W3ID makes a URI like this:</p>

<ul><li><code>https://w3id.org/mediatype/</code> + <code>{Media-Type}</code></li></ul>

<p>So for <code>text/html</code> we have:</p>

<ul><li><code>https://w3id.org/mediatype/text/html</code></li></ul>

<p>It's not rocket surgery...</p>

<p>Clicking on that URI yeilds a simple HTML view of the Media Type's properties. You can also get RDF data in a number of ways including by adding a <code>_format</code> query string argument to the URI with a Media Type value. Nicely self-referential huh?</p>
<p>To get RDF in the <a href="https://www.w3.org/TR/turtle/">Turtle</a> format for the Media Type <code>image/jpg</code>, use this URI:</p>
<ul><li><a href="https://w3id.org/mediatype/image/jpg?_format=text/turtle">https://w3id.org/mediatype/image/jpg<strong>?_format=text/turtle</strong></a></li></ul>

<h2>Code</h2>
<p>The code for this application is online at <a href="https://github.com/nicholascar/mediatypes-dataset">https://github.com/nicholascar/mediatypes-dataset</a>.</p>

<h2>License</h2>
<p>The content of this API is licensed for use under the GNU v3 License. See the <a href="https://www.gnu.org/copyleft/gpl.html">license deed</a> for details.</p>

<h2>Contacts</h2>
<p>If stuff breaks or doesn't work the way you expect it should or you want things extended, either add issues to the codebase (see above) or contact:</p>
<p>
    <strong>Nicholas Car</strong><br />
    <em>Senior Experimental Scientist</em><br />
    CSIRO Land &amp; Water, Environmental Informatics Group<br />
    Brisbane, Queensland<br />
    <a href="mailto:nicholas.car@csiro.au">nicholas.car@csiro.au</a><br />
    ORCID: <a href="https://orcid.org/0000-0002-8742-7730">0000-0002-8742-7730</a>
</p>
