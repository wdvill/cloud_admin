#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from peewee import ForeignKeyField, CharField, IntegerField, ForeignKeyField, DateTimeField, BooleanField
from .base import BaseModel
from common import utils

class Category(BaseModel):
    name = CharField(verbose_name="目录名称", max_length=100, null=False, default="")
    ename = CharField(verbose_name="英文名称", max_length=100, null=False, default="")
    description = CharField(verbose_name="详细", max_length=500, null=False, default="")
    level = IntegerField(verbose_name="目录级别", null=False, default=0)
    parent = ForeignKeyField('self', null=True, related_name='parent_category')
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class CategoryOptions(BaseModel):
    category = ForeignKeyField(Category)
    stage = BooleanField(null=False, default=False)
    language = BooleanField(null=False, default=False)
    api = BooleanField(null=False, default=False)
    framework = BooleanField(null=False, default=False)
    platform = CharField(max_length=200, null=False, default="")

    class Meta:
        db_table = "category_options"
