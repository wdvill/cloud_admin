#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
#from backend import misc, job, banner, feedback, category
from config.settings import all_skills, all_languages, all_frameworks
from common import utils

class Index(Base):
    def get(self):
        if not self.user:
            return self.redirect("/signin")

        return self.render("index.html")

