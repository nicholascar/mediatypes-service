import logging
import _conf as conf
from flask import Flask
from controller import routes
import pyldapi

app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)
app.register_blueprint(routes.routes)


# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    # generate the RDF sitemap
    thread = pyldapi.setup(app, conf.APP_DIR, conf.URI_BASE)

    # runn the Flask app
    app.run(debug=conf.DEBUG, use_reloader=False)

    # complete the RDF sitemap
    thread.join()
