# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, ForeignKeyField, DateTimeField, BooleanField, TextField, DecimalField
from .base import BaseModel
from .user import User
from .address import Address
from .attachment import Attachment
from common import utils

TEAM_TYPE = (
    ('client', '公司'),
    ('agency', '经纪人'),
)

MEMBER_TYPE = (
    ('owner', '创建者'),
    ('staff', '员工'),
)

class Team(BaseModel):
    user = ForeignKeyField(User, related_name="team")
    name = CharField(verbose_name="团队名称", max_length=150, null=False, default="")
    team_type = CharField(verbose_name="团队类型", max_length=10, null=False, default="", choices=TEAM_TYPE)
    status = CharField(verbose_name="团队状态", max_length=10, null=False, default="")
    location = ForeignKeyField(Address)
    logo = CharField(verbose_name="公司logo", max_length=200, null=False, default="")
    link = CharField(verbose_name="官网地址", max_length=100, null=False, default="")
    is_verify = BooleanField(verbose_name="是否认证", null=False, default=False)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    uuid = CharField(verbose_name="uuid", max_length=32, null=False, default=utils.generate_id, unique=True)
    trust_amount = DecimalField(verbose_name="托管金额", max_digits=8, decimal_places=2, default=0)
    expend_amount = DecimalField(verbose_name="累计支付", max_digits=8, decimal_places=2, default=0)

class Member(BaseModel):
    team = ForeignKeyField(Team, related_name="member")
    user = ForeignKeyField(User)
    mtype = CharField(verbose_name="成员类型", max_length=10, null=False, default="", choices=MEMBER_TYPE)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class TeamProfile(BaseModel):
    team = ForeignKeyField(Team, related_name="profile")
    overview = TextField(verbose_name="公司简介", null=False, default="")
    address = CharField(verbose_name="公司地址", max_length=100, null=False, default="")
    phone = CharField(verbose_name="公司电话", max_length=20, null=False, default="")
    email = CharField(verbose_name="公司邮箱", max_length=30, null=False, default="")
    company_name = CharField(verbose_name="公司名称", max_length=150, null=False, default="", help_text="审核通过之后，将该名称同步成团队名称")
    contact = CharField(verbose_name="公司联系人", max_length=20, null=False, default="")
    contact_phone = CharField(verbose_name="公司联系人电话", max_length=20, null=False, default="")
    permit_number = CharField(verbose_name="公司营业执照号", max_length=30, null=False, default="")
    org_number = CharField(verbose_name="公司组织机构代码号", max_length=30, null=False, default="")
    permit_img = ForeignKeyField(Attachment, related_name="permit_img", verbose_name="公司营业执照照片", null=True, default="0")
    org_img = ForeignKeyField(Attachment, related_name="org_img", verbose_name="公司组织机构代码照片", null=True, default="0")

    class Meta:
        db_table = "team_profile"
