#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import Model
from config.settings import database as dbn

class BaseModel(Model):
    class Meta:
        database = dbn
