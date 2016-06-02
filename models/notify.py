#-*- coding:utf-8 -*-

from peewee import CharField, DateTimeField, ForeignKeyField, BooleanField
from .base import BaseModel
from .user import User
from .team import Team
from common import utils

class Notify(BaseModel):
    # user 和 team同时只有一个
    user = ForeignKeyField(User, null=True)
    team = ForeignKeyField(Team, null=True)
    mtype = CharField(verbose_name="值", max_length=50, null=False, default="")
    read_at = DateTimeField(verbose_name="查看时间", null=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    extra = CharField(verbose_name="值", max_length=1000, null=False, default="")
    title = CharField(verbose_name="消息标题", max_length=100, null=False, default="")
    etitle = CharField(verbose_name="e消息标题", max_length=200, null=False, default="")
    content = CharField(verbose_name="消息内容", max_length=1000, null=False, default="")
    econtent = CharField(verbose_name="e消息内容", max_length=2000, null=False, default="")

class NotifySetting(BaseModel):
    user = ForeignKeyField(User, null=True)
    team = ForeignKeyField(Team, null=True)
    mtype = CharField(verbose_name="通知类型", max_length=30, null=False, default="")
    is_send = BooleanField(verbose_name="是否通知", null=False, default=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    class Meta:
        db_table="notify_setting"

class NotifyConfig(BaseModel):
    mtype = CharField(verbose_name="通知类型", max_length=30, null=False, default="")
    name = CharField(verbose_name="名称", max_length=100, null=False, default="")
    ename = CharField(verbose_name="英文名称", max_length=200, null=False, default="")
    who = CharField(verbose_name="角色", max_length=10, null=False, default="", help_text="f, c")
    class Meta:
        db_table="notify_config"
