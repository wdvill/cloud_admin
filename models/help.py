#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from peewee import ForeignKeyField, CharField, IntegerField, TextField, DateTimeField, BooleanField
from .base import BaseModel
from common import utils

class Topic(BaseModel):
    name = CharField(verbose_name="主题名", max_length="100", null=False, default="")
    ename = CharField(verbose_name="主题名(英文)", max_length="100", null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "help_topic"

class Question(BaseModel):
    uuid = CharField(verbose_name="uuid", max_length=32, null=False, default=utils.generate_id, unique=True, help_text="以md5代替uuid")
    topic = ForeignKeyField(Topic, related_name="question")
    title = CharField(verbose_name="问题名", max_length="100", null=False, default="")
    etitle = CharField(verbose_name="问题名(英文)", max_length="100", null=False, default="")
    answer = TextField(verbose_name="答案", null=False, default="")
    eanswer = TextField(verbose_name="答案(英文)", null=False, default="")
    hotspot = BooleanField(verbose_name="是否是热点问题", null=False, default=False)
    sortord = IntegerField(verbose_name="排序值", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)

    class Meta:
        db_table = "help_question"
