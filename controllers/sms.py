#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend.sms import send_verify_code


class SendVerifyCode(Base):
    def post(self):
        res = send_verify_code(self.user, self.params)
        return self.send(res)
