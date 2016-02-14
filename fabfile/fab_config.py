# -*- coding: utf-8 -*-
from time import gmtime, strftime
import os

from fabric.api import env

env.use_ssh_config = True

# Project
env.root = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 os.path.pardir)
)
env.project_name = 'badge'
env.project_path = env.root


# Web Machines
env.web_deploy_user = 'admin'
env.web_deploy_dir = '/home/%(web_deploy_user)s/www/%(project_name)s' % env

# Config
env.venv_name = "www" % env
env.venv_path = "/home/%(web_deploy_user)s/.virtualenvs/www/" % env
env.venv_python_path = "%(venv_path)s/lib/python2.7/site-packages" % env
env.activate = 'source %(venv_path)s/bin/activate' % env
env.python = 'python2'
env.utc_ts = gmtime()
env.utc_ts_str = strftime('%Y%m%d_%H%M%S', env.utc_ts)
