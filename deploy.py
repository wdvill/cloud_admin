#!/usr/bin/env python
# -*- coding:utf-8 -*-

from fabric.api import env, run, task, roles, cd, sudo, execute, parallel, prompt, prefix, put, hide, settings
from contextlib import contextmanager
from fabric.contrib.files import exists, contains
from fabric.colors import green, red, yellow


env.roledefs = { 
    'test': ["182.50.113.154"],
}

env.is_webpack = env.get("webpack")

def init_test_conf():
    env.user = "yunzujia"
    env.deploy_path = "/home/yunzujia/cloudwork/cloudwork"
    env.deploy_virt_path = "/home/yunzujia/cloudwork/env"
    env.activate = "source %s/bin/activate" % env.deploy_virt_path
    env.pip_install = "pip install -r %s/requirements.txt" % env.deploy_path
    env.branch = "master"

@roles("test")
def check_out():
    cd("~/")
    print(green("update cloudwork code"))
    with cd(env.deploy_path):
        run('git clean -f -d')
        #with settings(warn_only=True):
        with settings():
            result = run('git show-ref --verify --quiet refs/heads/%s' % env.branch)
            if result.return_code > 0:
                run('git fetch origin %s:%s' % (env.branch, env.branch))
                run("git checkout %s" % env.branch)
            else:
                run('git checkout %s' % env.branch)
                run('git pull origin %s' % env.branch)

@contextmanager
def virtualenv():
    with prefix("source %s/bin/activate" % env.deploy_virt_path):
        yield

@roles("test")
def restart_service():
    with virtualenv():
        with cd(env.deploy_path + "/migrations"):
            run("python upgrade.py")
            #run(env.pip_install)
        with settings():
            sudo("supervisorctl restart cloudwork")
            sudo("supervisorctl restart cloudwork-consume")
            if env.is_webpack == "true":
                with cd(env.deploy_path + "/rabbit"):
                    run("npm run publish")
            print(green("deploy ok, perfect!"))

def deploy_test():
    execute(init_test_conf)
    execute(check_out)
    execute(restart_service)
