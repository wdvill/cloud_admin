#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import resume


class Employment(Base):
    @signin_check
    def get(self):
        result = resume.employment_list(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    def post(self):
        result = resume.employment_add(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = resume.employment_change(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = resume.employment_remove(self.user, self.params)
        return self.send(result)


class Education(Base):
    @signin_check
    def get(self):
        result = resume.education_list(self.user, self.params)
        return self.send(result)

    @signin_check
    def post(self):
        result = resume.education_add(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = resume.education_change(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = resume.education_remove(self.user, self.params)
        return self.send(result)

class Portfolio(Base):
    @signin_check
    def get(self):
        result = resume.portfolio_list(self.user, self.params)
        return self.send(result)

    @signin_check
    def post(self):
        result = resume.portfolio_add(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = resume.portfolio_change(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = resume.portfolio_remove(self.user, self.params)
        return self.send(result)
