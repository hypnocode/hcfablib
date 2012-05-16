import os
from fabric.api import settings, local, abort
from fabric.contrib.console import confirm
import datetime


def check_git():
    with settings(warn_only=True):
        result = local('exit $(git status --porcelain | wc -l)')
    if result.failed:
        local('git status')
        if not confirm('uncommited changes (see above), continue anyway?'):
            abort('abort!')


def prepare_git():
    project_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
    local('git tag %s_deploy_%s' % (project_name, datetime.datetime.now().strftime('%F-%H-%M-%S')))
    local('git push --all')
    local('git push --tags')