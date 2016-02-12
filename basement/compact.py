# -*- coding: utf-8 -*-
try:
    from urllib import quote as urllib_quote
except ImportError:     # python3
    from urllib.parse import quote as urllib_quote

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

