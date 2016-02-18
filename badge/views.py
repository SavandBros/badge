# -*- coding: utf-8 -*-
import mimetypes
import gc

from klein import Klein
from twisted.web.static import File

from basement import settings
from basement.utils import render_template
from service import service_registry

app = Klein()


@app.route("/")
def index(request):
    return render_template('index.html')


@app.route("/static/", branch=True)
def static(request):
    return File(settings.STATIC_DIR)


@app.route('/<string:service>/<string:generator>/<string:package>/badge.<string:extension>')
def service_badge(request, service, generator, package, extension):
    gc.collect()

    if extension not in settings.ALLOWED_EXTENSIONS:
        request.setResponseCode(401)
        return "{} is not a valid extension.".format(extension)

    service_reg = service_registry.services.get(service, None)

    if not service_reg:
        request.setResponseCode(401)
        return "{} is not a valid service.".format(service)

    if generator not in service_reg['actions']:
        request.setResponseCode(401)
        return "{} is not a valid action.".format(generator)

    ext = mimetypes.types_map[".{0}".format(extension)]
    request.headers.update({'content-type': ext})

    service_class = service_reg['class']
    service_class = service_class(package, format=extension, extra_context=request.args)
    """:type service_class: service.base.ServiceBase"""
    service_class.pull_package_data()
    getattr(service_class, service_reg['actions'][generator])()
    img = service_class.draw_badge()

    return img
