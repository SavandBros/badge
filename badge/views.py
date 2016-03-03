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


@app.route("/bits/static/", branch=True)
def static(request):
    return File(settings.STATIC_DIR)


@app.route('/<string:service>/<string:package>/<string:markwhat>/')
def badge_markwhat(request, service, package, markwhat):
    gc.collect()
    markwhat = markwhat.lower()

    if markwhat not in settings.MARKWAHT_TEMPLATES:
        request.setResponseCode(400)
        return "{} is not a markwhat.".format(markwhat)

    service_reg = service_registry.services.get(service, None)

    if not service_reg:
        request.setResponseCode(400)
        return "{} is not a valid service.".format(service)

    badge_k51 = 'http://badge.kloud51.com'
    markwhat_template = settings.MARKWAHT_TEMPLATES[markwhat]
    markwhat_list = []
    service_actions = service_reg['actions']['actions']
    """:type service_actions: dict of (dict of str)"""
    service_class = service_reg['class'](package)
    """:type service_class: service.base.ServiceBase"""

    for k, v in service_actions.items():
        markwhat_list.append(markwhat_template.format(
            service_display=service_class.display_name,
            action_display=v['display_name'],
            action=v['short_name'],
            service=service,
            pkg_name=package,
            pkg_url=service_class.get_package_url(),
            badge_k51=badge_k51,
        ))

    request.headers.update({'content-type': 'txt'})

    return '\n'.join(markwhat_list)


@app.route('/<string:service>/<string:action>/<string:package>.<string:extension>')
def service_badge(request, service, action, package, extension):
    gc.collect()

    if extension not in settings.ALLOWED_EXTENSIONS:
        request.setResponseCode(401)
        return "{} is not a valid extension.".format(extension)

    service_reg = service_registry.services.get(service, None)

    if not service_reg:
        request.setResponseCode(401)
        return "{} is not a valid service.".format(service)

    if action not in service_reg['actions']['all']:
        request.setResponseCode(401)
        return "{} is not a valid action.".format(action)

    service_class = service_reg['class']
    service_class = service_class(package, format=extension, extra_context=request.args)
    """:type service_class: service.base.ServiceBase"""
    service_class.pull_package_data()

    if service_class.package_pulling_failed:
        request.setResponseCode(404)
        return "Couldn't pull data from {} for package {}".format(service, package)

    ext = mimetypes.types_map[".{0}".format(extension)]
    request.headers.update({'content-type': ext})

    getattr(service_class, service_reg['actions']['all'][action])()
    img = service_class.draw_badge()

    return img
