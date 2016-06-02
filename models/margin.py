#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, ForeignKeyField, DecimalField, DateTimeField
from .base import BaseModel
from .user import User
from .job import Job
from .team import Team
from common import utils

class Order(BaseModel):
    user = ForeignKeyField(User, related_name="order")
    trade_no = CharField(verbose_name='订单号', max_length=30, null=False, default="")
    parent = ForeignKeyField('self', null=True, related_name='parent_order', help_text="假如有子订单")
    request_ip = CharField(verbose_name="IP地址", max_length=20, null=False, default="")
    job = ForeignKeyField(Job, null=True)
    amount = DecimalField(verbose_name="交易金额", max_digits=8, decimal_places=2, default=0)
    fee = DecimalField(verbose_name="交易手续费", max_digits=8, decimal_places=2, default=0)
    status = CharField(verbose_name="订单状态", max_length=20, null=False, default="", help_text="fail, success, process")
    order_type = CharField(verbose_name="订单类型", max_length=20, null=False, default="", 
                            help_text="deposit, withdraw, pay, refund, freeze, income, bonus")
    confirm_at = DateTimeField(verbose_name="确认时间", null=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "order_order"

class PayInfo(BaseModel):
    user = ForeignKeyField(User, related_name="payinfo")
    order = ForeignKeyField(Order)
    card_no = CharField(verbose_name="银行卡号", max_length=20, null=False, default="")
    alipay = CharField(verbose_name="支付宝账号", max_length=50, null=False, default="")


class Bank(BaseModel):
    name = CharField(verbose_name='银行名字', max_length=50, null=False, default="")
    code = CharField(verbose_name="代码", max_length=20, null=False, default="")

class Card(BaseModel):
    bank = ForeignKeyField(Bank, related_name="card")
    user = ForeignKeyField(User, related_name="cards")
    card_no = CharField(verbose_name="银行卡号", max_length=20, null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class Margin(BaseModel):
    """账户"""
    user = ForeignKeyField(User, related_name="margin")
    margin = DecimalField(verbose_name="余额", max_digits=8, decimal_places=2, default=0)
    withdraw = DecimalField(verbose_name="提现中金额", max_digits=8, decimal_places=2, default=0)
    freeze = DecimalField(verbose_name="冻结金额", max_digits=8, decimal_places=2, default=0)
    income = DecimalField(verbose_name="累计收入", max_digits=8, decimal_places=2, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    update_at = DateTimeField(verbose_name="更新时间", null=False, default=utils.now)

mtype = (("deposit", "充值"), ("withdraw", "提现"), 
        ("pay", "支付"), ("income", "收入"),
        ("refund", "退款"), ("freeze", "冻结"),
        ("bonus", "奖金"),)

dtype = (("bonus", "奖金"),)

class MarginRecord(BaseModel):
    """账户变动记录"""
    user = ForeignKeyField(User, related_name="margin_record")
    team = ForeignKeyField(Team)
    amount = DecimalField(verbose_name="变动金额", max_digits=8, decimal_places=2, default=0)
    record_type = CharField(verbose_name="变动类型", max_length=20, null=False, default="", choices=mtype)
    record_desc = CharField(verbose_name="变动类型描述", max_length=20, null=False, default="", choices=dtype, help_text="二级分类")
    currently = DecimalField(verbose_name="变动前余额", max_digits=8, decimal_places=2, default=0)
    margin = DecimalField(verbose_name="变动后余额", max_digits=8, decimal_places=2, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    description = CharField(verbose_name="描述", null=False, default="")
    order = ForeignKeyField(Order, related_name="mrecord")

    class Meta:
        db_table = "margin_record"

