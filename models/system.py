# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField
from .base import BaseModel
from common import utils


PROFILE_IDENTIFY = (
    ('f', '开发者'),
    ('c', '企业需求者')
)

USER_STATUS = (
    ("unactive", "未启用"),
    ("active", "启用"),
    ("delete", "删除"),
)

class SystemUser(BaseModel):
    username = CharField(verbose_name="用户名", max_length=30, null=False, default="")
    password = CharField(verbose_name="密码", max_length=100, null=False, default="")
    salt = CharField(verbose_name="盐", max_length=20, null=False, default="")
    role_id = IntegerField(verbose_name="角色id", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "system_user"

class UserRole(BaseModel):
    user = ForeignKeyField(SystemUser)
    role_name = CharField(verbose_name="角色名", max_length=20, null=False, default="")
    update_at = DateTimeField(verbose_name="更新时间", null=True, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    class Meta:
        db_table = "system_user_role"
