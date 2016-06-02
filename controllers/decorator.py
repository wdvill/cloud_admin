#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import urllib

from backend.user import user_question
from common import utils


def client_check(func):
    def wrapper(params, *args):
        if params.user.identify[0] != "c":
            if params.is_mobile:
                return params.send({"error_code":30001, "msg":"not client"})
            #if params.request.method == "POST":
            #    return params.send({"error_code":405, "msg":"method not alowed"})
            return params.redirect("/find-work-home")
        return func(params, *args)
    return wrapper


def api_check(func):
    def wrapper(params):
        if not params.request.path.startswith("/api"):
            return params.send({"error_code":405, "msg":"method not alowed"})
        return func(params)
    return wrapper

def template_check(func):
    def wrapper(params, *args):
        if params.request.path.startswith("/api"):
            return params.send({"error_code":405, "msg":"method not alowed"})
        return func(params, *args)
    return wrapper

def signin_check(func):
    def wrapper(params, *args):
        if not params.user:
            if params.request.path.startswith("/api"):
                return params.send({"error_code":80001, "msg":"login required"})
            else:
                return params.redirect("/signin?next=%s" % urllib.quote_plus(params.request.path))
        #else:
        #    if params.is_mobile:
        #        i = params.params.get("i","")
        #        if i == "f" and params.user.identify[0] != "f":
        #            return params.send({"error_code":30002, "msg":"not freelancer"})
        #        elif i == "c" and params.user.identify[0] != "c":
        #            return params.send({"error_code":30001, "msg":"not client"})
        return func(params, *args)
    return wrapper

def freelancer_check(func):
    def wrapper(params, *args):
        if params.user.identify[0] != "f":
            if params.is_mobile:
                return params.send({"error_code":30002, "msg":"not freelancer"})
            #if params.request.method == "POST":
            #    return params.send({"error_code":405, "msg":"method not alowed"})
            return params.redirect("/jobs/new")
        return func(params, *args)
    return wrapper


def public_setting_verify(func):
    def wrapper(params, *args):
        qs = user_question(params.user)
        if qs['error_code'] != 0:
            return params.render("public-setting-question.html")
        
        if not params.user.last_verify or params.user.last_verify and (utils.now() - params.user.last_verify).days >= 1:
            return params.render("public-verify-password.html")
        
        return func(params, *args)
    return wrapper

