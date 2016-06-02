#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import api_check, signin_check
from backend import question


class QuestionRecord(Base):
    @api_check
    def get(self):
        result = question.question_list(self.params, self.lang)
        return self.send(result)
