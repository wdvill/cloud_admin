#-*- coding:utf-8 -*-

from peewee import CharField, DateTimeField
from .base import BaseModel
from common import utils

class Misc(BaseModel):
    misc_key = CharField(verbose_name="键", max_length=50, null=False, default="")
    value = CharField(verbose_name="值", max_length=1000, null=False, default="")
    description = CharField(verbose_name="描述", max_length=200, null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
