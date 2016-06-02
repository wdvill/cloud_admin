#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import traceback
import tornado.web
import logging
from tornado.httpclient import HTTPError
from config.settings import database, template, debug
from common.utils import dumps, now, md5
from models.session import Session
from backend.system_user import user_all_info

logger = logging.getLogger(__name__)

class Base(tornado.web.RequestHandler):
    def initialize(self):
        token = self.get_cookie("session_token")

        self.is_mobile, self.is_desktop = False, False

        self.user = None
        if token:
            session = Session.select().where(Session.session_key==token, Session.expire_at>now()).first()
            if session:
                self.user = session.user

        self.params = {key: value[-1] for key, value in self.request.arguments.items()}

    def send(self, result):
        if type(result) == dict:
            return self.write(dumps(result))
        return self.write(result)

    def render(self, template_path, **kwargs):
        user_all_info(self)
        kwargs.update(user=self.user)
        tmpl = template.get_template(template_path)
        self.finish(tmpl.render(**kwargs))

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super(Base, self).on_finish()

    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        raise HTTPError(405)

    def put(self, *args, **kwargs):
        raise HTTPError(405)

    def delete(self, *args, **kwargs):
        raise HTTPError(405)

    def options(self, *args, **kwargs):
        raise HTTPError(405)

    def head(self, *args, **kwargs):
        raise HTTPError(405)

    def write_error(self, status_code, **kwargs):
        lines = "".join(traceback.format_exception(*kwargs["exc_info"]))
        logger.error(lines)
        if debug:
            self.set_header('Content-Type', 'text/plain')
            self.write(lines)
        else:
            # define custom error page and handle
            #self.write("Internal server error")
            self.render("500.html")
        #self.finish()

    def prepare(self):
        self.xsrf_token

    def check_xsrf_cookie(self):
        #ua = self.request.headers.get("User-Agent", "")
        #if ua[:2] not in ("a/","i/","w/", "d/"):
        if not self.is_mobile:
            super(Base, self).check_xsrf_cookie()

class ErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with ``status_code`` for all requests."""
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise HTTPError(self._status_code)

    def check_xsrf_cookie(self):
        # POSTs to an ErrorHandler don't actually have side effects,
        # so we don't need to check the xsrf token.  This allows POSTs
        # to the wrong url to return a 404 instead of 403.
        pass 

class NoCSRFBase(Base):
    def check_xsrf_cookie(self):
        pass

class EncryptBase(Base):
    def initialize(self):
        super(EncryptBase, self).initialize()
        res = self.decrypt()
        if res:
            self.send(res)
            self._transforms = []

            self.finish()

    def check_xsrf_cookie(self):
        pass

    def decrypt(self):
        if "sign" not in self.params or "stamp" not in self.params:
            return {"error_code":80005, "msg":"parameter not enough"}
        sign = self.params.pop("sign")
        keys = sorted(self.params)
        sign_str = "".join(["%s=%s" % (k,self.params[k]) for k in keys])
        if md5(sign_str + "cloudwork") != sign:
            return {"error_code":80006, "msg":"sign error"}
