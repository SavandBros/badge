# -*- coding: utf-8 -*-

from fabric.operations import local

from fabfile import env
from fabfile.utils import grint, grintify


@grintify
def set_env(env_name):
    """
    Set `env.env_name`.
    """
    grint('Set env_name to {0}'.format(env_name))
    env.env_name = env_name


@grintify
def clean_pyc():
    """
    Clean python compiled files (*.pyc)
    """
    local("find %(root)s/ -name '*.pyc' -delete" % env)
