# -*- coding: utf-8 -*-
import logging

from fabric.operations import prompt, local

import git
from slugify import slugify
from fabfile.utils import grintify, grint
from fabfile.fab_config import env

try:
    repo = git.Repo(env.root)
except git.exc.InvalidGitRepositoryError:
    logging.error("Not git repo found!")


def _git(cmd):
    local('git {0}'.format(cmd))


@grintify
def git_push():
    """
    Push the repository to remote
    """
    _git('push origin master')


@grintify
def git_pull():
    """
    Pull the changes from origin remote branch
    """
    _git("pull")


@grintify
def git_add_dot():
    """
    run "git add ."
    """
    _git("add .")


@grintify
def new_branch():
    """
    Creating new branch
    """
    branch_type = slugify((prompt('Branch type:', default='feature')))
    issue_id = prompt("Issue ID:")
    short_description = slugify(prompt('Short description:'))

    if not branch_type or not short_description:
        raise ValueError('[Branch type] and [Short description] are'
                         'mandatory.')

    if issue_id:
        issue_id = '-#{0}'.format(issue_id)

    branch_name = "{0}{1}-{2}".format(branch_type, issue_id, short_description)
    ru_sure = prompt(
        text='Branch name will be "{0}", Are sure? (y/n)'.format(branch_name),
        default='y'
    )

    if ru_sure != 'y':
            return

    _git('checkout -b "{0}"'.format(branch_name))


def branch_push():
    """
    Pushing changes to remote branch.
    """
    grint(u"Pushing changes to branch: [{0}]".format(repo.active_branch))

    repo.git.push('origin', repo.active_branch)
