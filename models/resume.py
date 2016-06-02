#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from common import utils
from peewee import ForeignKeyField, DateField, CharField, IntegerField, TextField, DecimalField, DateTimeField, BooleanField, FixedCharField
from .base import BaseModel
from .address import Address
from .attachment import Attachment
from .category import Category
from .user import User


# 工作经历
class Employment(BaseModel):
    user = ForeignKeyField(User)
    company = CharField(verbose_name="公司名称", max_length=100, null=False)
    city = ForeignKeyField(Address, verbose_name="所在城市")
    country = CharField(verbose_name="所在国家", max_length=50, null=True, default="")
    title = CharField(verbose_name="职位", max_length=50, null=False)
    role = IntegerField(verbose_name="角色", null=False, default="0")
    start_at = DateTimeField(verbose_name="开始日期", null=False)
    end_at = DateTimeField(verbose_name="截止日期", null=False)
    working = BooleanField(verbose_name="是否在职", null=False, default=False)
    detail = TextField(verbose_name="工作描述", null=True, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)

# 教育经历
class Education(BaseModel):
    user = ForeignKeyField(User)
    start_at = DateField(verbose_name="开始日期", null=False)
    end_at = DateField(verbose_name="截止日期", null=False)
    school = CharField(verbose_name="学校", max_length=100, null=False)
    degree = CharField(verbose_name="学位", max_length=20, null=False)
    area = CharField(verbose_name="学习专业", max_length=100, null=False)
    detail = TextField(verbose_name="教育描述", null=True, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)

# 所获得的证书
class Certification(BaseModel):
    pass

# 项目列表
class Portfolio(BaseModel):
    user = ForeignKeyField(User)
    name = CharField(verbose_name="项目名称", max_length=100, null=False)
    detail = TextField(verbose_name="项目描述", null=False)
    attachment = ForeignKeyField(Attachment, related_name="attachment_to_project")
    picture = ForeignKeyField(Attachment, verbose_name="项目图片", related_name="picture_to_project")
    category = ForeignKeyField(Category)
    link = CharField(verbose_name="项目地址", max_length=100, null=True, default="")
    end_at = DateField(verbose_name="完成时间", null=True)
    skills = CharField(verbose_name="技能", max_length=1000, null=False, default="", help_text="存放数组字符串")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)
