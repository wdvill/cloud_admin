# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, BooleanField, DateTimeField, IntegerField, TextField, ForeignKeyField, DecimalField
from .base import BaseModel
from common import utils
from .category import Category
from .question import Question
from .address import Address


PROFILE_IDENTIFY = (
    ('f', '开发者'),
    ('c', '企业需求者')
)

USER_STATUS = (
    ("unactive", "未启用"),
    ("active", "启用"),
    ("delete", "删除"),
)


class User(BaseModel):
    username = CharField(verbose_name="用户名", max_length=30, null=False, default="")
    password = CharField(verbose_name="密码", max_length=100, null=False, default="")
    salt = CharField(verbose_name="盐", max_length=20, null=False, default="")
    email = CharField(verbose_name="邮箱", max_length=50, null=False, default="")
    phone = CharField(verbose_name="手机号", max_length=20, null=False, default="")
    area = CharField(verbose_name="手机号国家代码", max_length=15, null=False, default="")
    emailverify = BooleanField(verbose_name="邮箱验证", null=False, default=False)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    #verifycode = CharField(verbose_name="验证码", max_length=10, null=False, default="")
    #update_at = DateTimeField(verbose_name="时间", null=False, default=utils.now)

    ## [c|f|p][id]
    ## c means client, f means freelancer
    identify = CharField(verbose_name="当前登录身份", max_length=20, null=False)
    status = CharField(verbose_name="用户状态", max_length=20, null=False, choices=USER_STATUS, default="unactive", help_text="默认未启用")
    reg_step = CharField(verbose_name="注册步骤", max_length=20, null=False, default="", 
                help_text="category, profile, resume, other, success")
    last_verify = DateTimeField(verbose_name="时间", null=True)
    uuid = CharField(verbose_name="uuid", max_length=32, null=False, default=utils.generate_id, unique=True)
    to_dev = BooleanField(verbose_name="开发者身份", null=False, default=False, help_text="是否创建了开发者身份")
    to_req = BooleanField(verbose_name="需求者身份", null=False, default=False, help_text="是否创建了需求者身份")
    app_identify = CharField(verbose_name="当前登录身份", max_length=20, null=False, default="")


class Profile(BaseModel):
    user = ForeignKeyField(User, related_name="profile")
    name = CharField(verbose_name="姓名", max_length=30, null=False, default="")
    avatar = CharField(verbose_name="头像", max_length=200, null=False, default="")
    completeness = IntegerField(verbose_name="资料完整度", null=False, default=0, help_text="0-100的数值")
    visibility = BooleanField(verbose_name="是否可见", null=False, default=True)
    level = CharField(verbose_name="技能等级", max_length=10, null=False, default="")
    title = CharField(verbose_name="职位描述", max_length=30, null=False, default="")
    overview = TextField(verbose_name="详细简介", null=True, default="")
    hourly = DecimalField(verbose_name="时薪", max_digits=7, decimal_places=2, null=False, default=0)
    english = CharField(verbose_name="英语等级", max_length=10, null=False, default="")
    skills = TextField(verbose_name="技能列表", null=True, default="")
    available = BooleanField(verbose_name="是否可工作", null=False, default=True)
    workload = IntegerField(verbose_name="每周可工作小时", null=False, default=0)
    location = ForeignKeyField(Address, null=False, default=0)
    address = CharField(verbose_name="地址", max_length=100, null=False, default="")
    postcode = CharField(verbose_name="邮编", max_length=20, null=False, default="")
    is_notice = BooleanField(verbose_name="是否接收推送", null=False, default=False)
    id_number = CharField(verbose_name="身份证号", max_length=20, null=False, default="")
    alipay = CharField(verbose_name="支付宝账号", max_length=50, null=False, default="")
    coop_rate = IntegerField(verbose_name="工作成功率", null=False, default=0)
    recomm_rate = CharField(verbose_name="推荐工作频率", max_length=20, null=False, default="")
    last_recomm = DateTimeField(verbose_name="上次推荐日期", null=True)


class Party(BaseModel):
    user = ForeignKeyField(User, related_name="party")
    vip = BooleanField(verbose_name="是否收费会员", null=False, default=False)
    connects = IntegerField(verbose_name="剩余豆豆", null=False, default=0)
    agency_vip = BooleanField(verbose_name="代理人是否收费会员", null=False, default=False)
    agency_connects = IntegerField(verbose_name="代理人剩余豆豆", null=False, default=0)
    vip_thur_at = DateTimeField(verbose_name="会员失效日期", null=True)
    agency_thur_at = DateTimeField(verbose_name="会员失效日期", null=True)

class UserCategory(BaseModel):
    user = ForeignKeyField(User, related_name="category")
    category = ForeignKeyField(Category)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "user_category"

class UserLanguage(BaseModel):
    user = ForeignKeyField(User, related_name="language")
    name = CharField(verbose_name="语言名字", max_length=30, null=False)
    level = CharField(verbose_name="水平等级", max_length=20, null=False)

    class Meta:
        db_table = "user_language"


class UserQuestion(BaseModel):
    user = ForeignKeyField(User)
    question = ForeignKeyField(Question)
    answer = CharField(verbose_name="问题答案", max_length=100, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "user_question"


class UserPoints(BaseModel):
    user = ForeignKeyField(User)
    category = BooleanField(verbose_name="是否设置分类", null=False, default=False)
    avatar = BooleanField(verbose_name="是否设置头像", null=False, default=False)
    title = BooleanField(verbose_name="是否设置职位", null=False, default=False)
    overview = BooleanField(verbose_name="是否设置简介", null=False, default=False)
    email = BooleanField(verbose_name="是否设置邮箱", null=False, default=False)
    skills = BooleanField(verbose_name="是否设置技能", null=False, default=False)
    english = BooleanField(verbose_name="是否设置英语水平", null=False, default=False)
    other_language = BooleanField(verbose_name="是否设置其它语言", null=False, default=False)
    workload = BooleanField(verbose_name="是否设置可工作时长", null=False, default=False)
    level = BooleanField(verbose_name="是否设置经验水平", null=False, default=False)
    employment = BooleanField(verbose_name="是否设置工作经历", null=False, default=False)
    education = BooleanField(verbose_name="是否设置教育经历", null=False, default=False)
    portfolio = BooleanField(verbose_name="是否设置项目经历", null=False, default=False)
    hourly = BooleanField(verbose_name="是否设置时薪", null=False, default=False)
    location = BooleanField(verbose_name="是否设置所在城市", null=False, default=False)
    address = BooleanField(verbose_name="是否设置详细地址", null=False, default=False)
    postcode = BooleanField(verbose_name="是否设置邮编", null=False, default=False)

    class Meta:
        db_table = "user_points"

class UserRole(BaseModel):
    user = ForeignKeyField(User)
    rtype = CharField(verbose_name="身份", max_length=20, null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    class Meta:
        db_table = "user_role"
