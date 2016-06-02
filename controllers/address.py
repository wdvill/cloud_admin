#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import address

class AddressRecord(Base):
    def get(self):
        result = address.address_list(self.params, self.lang)
        return self.send(result)
