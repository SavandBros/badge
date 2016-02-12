# -*- coding: utf-8 -*-
import mimetypes
import os

from badge import app
from basement.settings import FILE_CACHE

if not os.path.exists(FILE_CACHE):
    print("Creating {0} cache dir".format(FILE_CACHE))
    os.makedirs(FILE_CACHE)

resource = app.resource

if __name__ == '__main__':
    if not os.path.exists(FILE_CACHE):
        os.mkdir(FILE_CACHE)
    if '.svg' not in mimetypes.types_map:
        mimetypes.add_type("image/svg+xml", ".svg")

    app.run("localhost", 80)
