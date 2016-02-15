# -*- coding: utf-8 -*-
import mimetypes
import os

from badge.views import app
from basement.settings import FILE_CACHE

if not os.path.exists(FILE_CACHE):
    print("Creating {0} cache dir".format(FILE_CACHE))
    os.makedirs(FILE_CACHE)

if '.svg' not in mimetypes.types_map:
    mimetypes.add_type("image/svg+xml", ".svg")

resource = app.resource

if __name__ == '__main__':
    app.run("localhost", 80)
