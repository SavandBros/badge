# -*- coding: utf-8 -*-
import mimetypes
import gc

from klein import Klein

from shields.shields import generators

app = Klein()


@app.route('/<string:generator>/<string:package>/badge.<string:extension>')
def shield(request, generator, package, extension):
    gc.collect()
    ext = mimetypes.types_map[".{0}".format(extension)]
    request.headers.update({'content-type': ext})
    klass = generators[generator]()
    img = klass.get(request, package, extension)

    return img
