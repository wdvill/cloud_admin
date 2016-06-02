#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, BooleanField, IntegerField
from .base import BaseModel
from common import utils

class Banner(BaseModel):
    title = CharField(verbose_name="名字", max_length=100, null=False, default="")
    image = CharField(verbose_name="图片", max_length=200, null=False, default="")
    link = CharField(verbose_name="链接", max_length=200, null=False, default="")
    platform = CharField(verbose_name="平台", max_length=20, null=False, default="", help_text="web, app, ios, android")
    visible = BooleanField(verbose_name="是否可见", null=False, default=True)
    sortord = IntegerField(verbose_name="排序", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
