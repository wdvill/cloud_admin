# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField, TextField, DecimalField, BooleanField
from .base import BaseModel
from .user import User
from .job import Job
from .team import Team
from .attachment import Attachment
from .question import Question
from .margin import Order, MarginRecord
from common import utils


class Contract(BaseModel):
    user = ForeignKeyField(User, help_text="只会是开发者")
    job = ForeignKeyField(Job, related_name="contract")
    team = ForeignKeyField(Team)
    name = CharField(verbose_name="合同名称", max_length=100, null=False, default="")
    invoice = CharField(verbose_name="合同编号", max_length=30, null=False, default="")
    amount = DecimalField(verbose_name="合同金额", max_digits=12, decimal_places=2, null=False, default=0)
    hourly = DecimalField(verbose_name="合同时薪", max_digits=8, decimal_places=2, null=False, default=0)
    workload = IntegerField(verbose_name="每周需要工作小时(具体小时数,大于1)", null=False, default=0)
    status = CharField(verbose_name="合同状态", max_length=20, null=False, default="", 
                        help_text="unpaid(未支付), revoke(撤消), refuse(拒绝), paid(已支付), carry(执行), pause, finish, expire(过期), dispute, service")
    stone_status = CharField(verbose_name="里程碑付款状态", max_length=20, null=False, default="", help_text="carry_pay(已支付), carry(执行)")
    total_amount = DecimalField(verbose_name="合同最终支付", max_digits=12, decimal_places=2, null=False, default=0)
    message = CharField(verbose_name="附加消息", max_length=500, null=False, default="")
    attachment = ForeignKeyField(Attachment)
    question = ForeignKeyField(Question)
    order = ForeignKeyField(Order)
    reason = CharField(verbose_name="拒绝原因", max_length=500, null=False, default="")
    start_at = DateTimeField(verbose_name="合同开始时间", null=True)
    end_at = DateTimeField(verbose_name="合同结束时间", null=True)
    uuid = CharField(verbose_name="uuid", max_length=32, null=False, default=utils.generate_id, unique=True)
    finish_by = CharField(verbose_name="开发者or需求者关闭", max_length=20, null=False, default="", help_text="user, team")
    accept_at = DateTimeField(verbose_name="接受时间", null=True)
    expire_at = DateTimeField(verbose_name="合同过期时间", null=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)
    actual_end_at = DateTimeField(verbose_name="实际截止时间", null=True)
    user_evl = IntegerField(verbose_name="开发者评价", null=False, default=0)
    team_evl = IntegerField(verbose_name="需求者评价", null=False, default=0)
    manual  = BooleanField(verbose_name="是否允许人工计时", null=False, default=False, help_text="只有设置了人工计时，计时软件才允许手工上传截图")


# 按小时没有里程碑
class MileStone(BaseModel):
    contract = ForeignKeyField(Contract, related_name="milestone")
    name = CharField(verbose_name="里程碑名称", max_length=100, null=False, default="")
    amount = DecimalField(verbose_name="原始金额", max_digits=8, decimal_places=2, null=False, default=0)
    actual_amount = DecimalField(verbose_name="实际支付", max_digits=8, decimal_places=2, null=False, default=0)
    status = CharField(verbose_name="里程碑状态", max_length=20, null=False, default="", 
                        help_text="paid, refuse, finish, carry, carry_pay, service, dispute, cancel")
    order = ForeignKeyField(Order, related_name="milestone_order", help_text="充值的order_id")
    pay_order = ForeignKeyField(Order, related_name="milestone_pay_order", help_text="付款的order_id")
    term = IntegerField(verbose_name="第几期", null=False, default=0)
    start_at = DateTimeField(verbose_name="开始时间", null=True)
    end_at = DateTimeField(verbose_name="结束时间", null=True)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

# 提交付款，交流记录
class MileStoneRecord(BaseModel):
    milestone = ForeignKeyField(MileStone, related_name="record")
    attachment = ForeignKeyField(Attachment)
    audit_attachment = ForeignKeyField(Attachment, related_name="audit_attachment")
    message = CharField(verbose_name="消息", max_length=500, null=False, default="")
    reason = CharField(verbose_name="消息", max_length=500, null=False, default="")
    audit_at = DateTimeField(verbose_name="审核时间", null=True)
    create_at = DateTimeField(verbose_name="提交时间", null=True, default=utils.now)

    class Meta:
        db_table = "milestone_record"

# 按小时也按里程碑的方式结算
class WeekStone(BaseModel):
    contract = ForeignKeyField(Contract, related_name="weekstone")
    amount = DecimalField(verbose_name="原始金额", max_digits=8, decimal_places=2, null=False, default=0)
    actual_amount = DecimalField(verbose_name="实际支付", max_digits=8, decimal_places=2, null=False, default=0)
    status = CharField(verbose_name="本周工作状态", max_length=20, null=False, default="", 
                        help_text="paid, refuse, finish, cancel, carry, carry_pay, service, dispute")
    order = ForeignKeyField(Order, related_name="weekstone_order")
    pay_order = ForeignKeyField(Order, related_name="weekstone_pay_order", help_text="付款的order_id")
    start_at = DateTimeField(verbose_name="开始时间", null=True)
    end_at = DateTimeField(verbose_name="结束时间", null=True)
    term = IntegerField(verbose_name="第几期", null=False, default=0)
    shot_times = IntegerField(verbose_name="记录次数", null=False, default=0)
    manual_times = IntegerField(verbose_name="手工记录次数", null=False, default=0)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class WeekStoneRecord(BaseModel):
    weekstone = ForeignKeyField(WeekStone, related_name="record")
    audit_attachment = ForeignKeyField(Attachment)
    reason = CharField(verbose_name="消息", max_length=500, null=False, default="")
    audit_at = DateTimeField(verbose_name="审核时间", null=True)
    create_at = DateTimeField(verbose_name="提交时间", null=False, default=utils.now)

    class Meta:
        db_table = "weekstone_record"

class ShotRecord(BaseModel):
    """ 截屏记录 """
    weekstone = ForeignKeyField(WeekStone, related_name="shot")
    attachment = ForeignKeyField(Attachment, null=True)
    user = ForeignKeyField(User, help_text="只会是开发者")
    team = ForeignKeyField(Team)
    name = CharField(verbose_name="记录名字", max_length=50, null=False, default="")
    shot_at = DateTimeField(verbose_name="截屏时间", null=False)
    hour = IntegerField(verbose_name="几点", null=False, default=0, help_text="加上小时方便统计")
    activity = IntegerField(verbose_name="活跃度", null=False, default=0)
    keyboard = IntegerField(verbose_name="键盘次数", null=False, default=0)
    mouse = IntegerField(verbose_name="鼠标次数", null=False, default=0)
    is_auto = BooleanField(verbose_name="是否自动提交", null=False, default=False)
    description = CharField(verbose_name="描述", max_length=500, null=False, default="")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

class ContractRecord(BaseModel):
    contract = ForeignKeyField(Contract)
    rtype = CharField(verbose_name="记录类型", max_length=20, null=False, default="")
    extra = TextField(verbose_name="扩展字段", null=False, default="", help_text="存储json,每种类型需要不同字段")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "contract_record"

class WeekStoneReport(BaseModel):
    user = ForeignKeyField(User, help_text="只会是开发者")
    team = ForeignKeyField(Team)
    contract = ForeignKeyField(Contract)
    weekstone = ForeignKeyField(WeekStone)
    period = IntegerField(verbose_name="日期8位数", null=False, default=0)
    times = IntegerField(verbose_name="当天记录次数", null=False, default=0)
    hourly = DecimalField(verbose_name="合同时薪", max_digits=8, decimal_places=2, null=False, default=0)
    status = CharField(verbose_name="状态", max_length=20, null=False, default="", help_text="finish(已完成), carry(执行)")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "weekstone_report"

class MarginContractRecord(BaseModel):
    margin_record = ForeignKeyField(MarginRecord, related_name="margin_record_contract")
    contract = ForeignKeyField(Contract, related_name="margin_contract")
    milestone = ForeignKeyField(MileStone, related_name="margin_milestone", null=True, default=0)
    weekstone = ForeignKeyField(WeekStone, related_name="margin_weekstone", null=True, default=0)
    order = ForeignKeyField(Order, related_name="mrecord_order")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "margin_contract_record"

class ContractEvaluate(BaseModel):
    contract = ForeignKeyField(Contract)
    exchange = IntegerField(verbose_name="沟通得分", null=False, default=0)
    punctual = IntegerField(verbose_name="守时得分(需求者)", null=False, default=0)
    cooper = IntegerField(verbose_name="合作得分", null=False, default=0)
    quality = IntegerField(verbose_name="质量得分", null=False, default=0)
    skill = IntegerField(verbose_name="技能得分", null=False, default=0)
    avail = IntegerField(verbose_name="可用性得分(开发者)", null=False, default=0)
    deliver = IntegerField(verbose_name="合理设计交付时间得分(开发者)", null=False, default=0)
    content = CharField(verbose_name="评价内容", null=False, max_length=500, default="")
    identify = CharField(verbose_name="评价的身份", null=False, max_length=20, default="", help_text="f, c")
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "contract_evaluate"

class OrderBonus(BaseModel):
    order = ForeignKeyField(Order)
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
    freelancer = ForeignKeyField(User, related_name="freelancer")
    amount = DecimalField(verbose_name="交易金额", max_digits=8, decimal_places=2, default=0)
    fee = DecimalField(verbose_name="交易手续费", max_digits=8, decimal_places=2, default=0)
    pay_order = ForeignKeyField(Order, related_name="order_freelancer")
    contract = ForeignKeyField(Contract, null=True)
    status = CharField(verbose_name="订单状态", max_length=20, null=False, default="", help_text="fail, success, process")
    description = CharField(verbose_name="描述", null=False, default="")
    confirm_at = DateTimeField(verbose_name="创建时间", null=False)
    create_at = DateTimeField(verbose_name="创建时间", null=False, default=utils.now)

    class Meta:
        db_table = "order_bonus"

