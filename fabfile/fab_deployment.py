# -*- coding: utf-8 -*-
from contextlib import contextmanager

from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo

from fabfile.utils import grintify
from fabfile import env


@grintify
@contextmanager
def venv():
    """
    Activate the virtualenv
    """
    with cd(env.venv_path):
        with prefix(env.activate):
            yield


@grintify
def deploy():
    """
    Deploy the project to production server
    """
    deploy_web_hosts()


@grintify
def set_web_hosts():
    """
    Set targets to Web machines
    """
    env.user = env.web_deploy_user
    env.hosts = ['badge.kloud51.com', ]


@grintify
def deploy_web_hosts():
    """
    Deploy to web machines
    """
    with venv():
        with cd(env.web_deploy_dir):
            run('git pull origin master')
            run('pip install -r requirements/dev.txt')
            run('fab clean_pyc')
            sudo('systemctl restart badgek51')
