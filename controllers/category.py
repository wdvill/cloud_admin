#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import category

class CategoryList(Base):
    def post(self):
        result = category.category_list(self.params, self.lang)
        return self.send(result)

class CategoryOptions(Base):
    def get(self):
        result = category.get_category_option(self.params)
        return self.send(result)
