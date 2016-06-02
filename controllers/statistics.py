#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, freelancer_check

from backend import statistics 


# 不再使用
class UserStatistics(Base):
    def get(self):
        result = statistics.user_statistics(self.params)
        return self.send(result)

