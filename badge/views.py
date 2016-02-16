# -*- coding: utf-8 -*-
import mimetypes
import gc

from klein import Klein

from twisted.web.static import File

from basement import settings
from basement.utils import render_template
from service import generators

app = Klein()


@app.route("/")
def index(request):
    return render_template('index.html')


@app.route("/static/", branch=True)
def static(request):
    return File(settings.STATIC_DIR)


@app.route('/<string:service>/<string:generator>/<string:package>/badge.<string:extension>')
def shield(request, service, generator, package, extension):
    gc.collect()

    if extension not in settings.ALLOWED_EXTENSIONS:
        request.setResponseCode(401)
        return "{} is not a valid extension.".format(extension)

    ext = mimetypes.types_map[".{0}".format(extension)]
    request.headers.update({'content-type': ext})
    klass = generators[service][generator]()
    img = klass.get(request, package, extension)

    return img
