#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, IntegerField, DateTimeField, ForeignKeyField
from .base import BaseModel
from common import utils

class Address(BaseModel):
    name = CharField(verbose_name="地点名字", max_length=100, null=False, default="")
    level = IntegerField(verbose_name="级别", null=False, default=0)
    parent = ForeignKeyField('self', null=True, related_name='address_parent', help_text="三级联动")
    code = CharField(verbose_name="手机区号", max_length=100, null=False, default="", help_text="国家才有")
    ename = CharField(verbose_name="地点英文", max_length=150, null=False, default="", help_text="中文地址为拼音")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
