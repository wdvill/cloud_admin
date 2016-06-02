#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import ForeignKeyField, CharField, IntegerField, TextField, DecimalField, DateTimeField, BooleanField
from .base import BaseModel
from .user import User
from .team import Team
from .category import Category
from .attachment import Attachment
from common import utils

class Job(BaseModel):
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
    name = CharField(verbose_name="工作名称", max_length=100, null=False, default="")
    category = ForeignKeyField(Category)
    skills = CharField(verbose_name="技能", max_length=1000, null=False, default="", help_text="存放数组字符串")
    duration = IntegerField(verbose_name="持续时间", null=False, default=0)
    workload = IntegerField(verbose_name="每周需要工作小时", null=False, default=0)
    level = CharField(verbose_name="需要开发者技能等级", max_length=10, null=False, default="", help_text="entry, middle, expert")
    hires = IntegerField(verbose_name="招聘人数", null=False, default=0)
    attachment = ForeignKeyField(Attachment)
    summary = CharField(verbose_name="详情摘要", max_length=100, null=False, default="")
    description = TextField(verbose_name="详细描述", null=True, default="")
    stage = CharField(verbose_name="项目进行阶段", max_length=20, null=False, default="")
    budget = DecimalField(verbose_name="预算", max_digits=10, decimal_places=2, default=0)
    paymethod = CharField(verbose_name="付款方式", max_length=10, null=False, default="", help_text="hour，fixed")
    status = CharField(verbose_name="状态", max_length=10, null=False, default="normal", choices=(("normal", "正常"), ("draft", "草稿"), ("delete", "删除"), ("close", "关闭")))
    platforms = CharField(verbose_name="针对的平台", max_length=100, null=False, default="")
    integrated_api = CharField(verbose_name="对接api", max_length=100, null=False, default="")
    languages = CharField(verbose_name="语言", max_length=100, null=False, default="", help_text="存放数组字符串")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)
    job_uuid = CharField(verbose_name="uuid", max_length=32, null=False, default=utils.generate_id, unique=True, help_text="以md5代替uuid")
    frameworks = CharField(verbose_name="软件框架", max_length=200, null=False, default="")
    last_view_time = DateTimeField(verbose_name="最后一次查看时间", null=False, default=utils.now)
