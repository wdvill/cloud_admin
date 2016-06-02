#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import attachment

class Upload(Base):
    @signin_check
    def post(self):
        if "file" not in self.request.files:
            return self.send({"error_code":20043, "msg":"upload parameters not enough"})

        result = attachment.upload(self.user, self.params, self.request.files['file'][0])
        return self.send(result)

class Download(Base):
    @signin_check
    def get(self, path):
        self.params['path'] = path
        result = attachment.download(self.params)
        if result['error_code']:
            return self.send(result)
        return self.redirect(result['download_url'])
