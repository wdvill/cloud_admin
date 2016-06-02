#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, client_check, freelancer_check

class Concatus(Base):
    def get(self):
        return self.render("mobile/concatus.html")
