#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import favorite

class Favorite(Base):
    @signin_check
    def get(self):
        result = favorite.favorite_list(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    def post(self):
        result = favorite.favorite_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = favorite.favorite_delete(self.user, self.params)
        return self.send(result)

# 我的订阅
class Subscribe(Base):
    @signin_check
    def get(self):
        result = favorite.subscribe_list(self.user, self.params)
        return self.send(result)

    @signin_check
    def post(self):
        result = favorite.subscribe_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = favorite.subscribe_delete(self.user, self.params)
        return self.send(result)
