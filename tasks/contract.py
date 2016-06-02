#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import datetime
import decimal
import logging
import traceback

from common import utils, queue
from config.settings import database
from models.contract import Contract, WeekStone, ShotRecord, WeekStoneRecord, WeekStoneReport
from backend import margin

logger = logging.getLogger(__name__)

def check_offer_expire(body):
    # offer 2 天没处理就过期，钱退回到账户
    now = utils.now()
    start = utils.timedelta(now, days=-2)
    # TODO 分页
    records = Contract.select().where(Contract.create_at<=start, Contract.status=='paid')
    for contract in records:
        with database.atomic() as txn:
            try:
                contract.status = "expire"
                contract.expire_at = now
                contract.save()
                margin.refund_amount(contract.team.user, contract.team, contract.job, contract.amount)
                # send msg to user
                queue.to_queue({"type": "contract_expire", "contract_id": contract.id})
            except:
                txn.rollback()

# 时薪里程碑到一周之后自动提审
def count_weekstone(body):
    now = utils.now()
    start = utils.timedelta(now, days=-7)
    day_start = utils.datetime_day_min(start)
    day_end = utils.datetime_day_max(start)

    weekstones = WeekStone.select().where(WeekStone.start_at.between(day_start, day_end))
    for ws in weekstones:
        # 合同状态和时薪周状态都是进行中的才自动提审
        if ws.contract.status != "carry":
            continue
        if ws.status != "carry":
            continue

        with database.atomic() as txn:
            try:
                record = WeekStoneRecord()
                record.weekstone = ws
                record.save()

                ws.status = "carry_pay"
                ws.contract.stone_status = "carry_pay"
                ws.contract.save()
                ws.save()
                queue.to_queue({"type": "weekstone_freelancer_audit", "weekstone_id": ws.id})
            except:
                txn.rollback()

# 超过两天没处理，自动打款
def auto_pay_weekstone(body):
    now = utils.now()
    start = utils.timedelta(now, days=-2)
    start = utils.now()
    records = WeekStoneRecord.select().where(WeekStoneRecord.create_at<=start, WeekStoneRecord.audit_at.is_null(True))
    for rd in records:
        ws = rd.weekstone
        if ws.status != "carry_pay":
            continue
        contract = ws.contract
        if contract.status != "carry":
            continue

        with database.atomic() as txn:
            try:
                if ws.shot_times > contract.workload * 6:
                    pay_times = contract.workload * 6
                    amount = contract.amount
                else:
                    pay_times = ws.shot_times
                    amount = utils.decimal_two(contract.hourly * ws.shot_times / 6)
                ws.actual_amount = amount
                ws.status = "finish"
                ws.end_at = now

                order = margin.payment_freelancer(contract.team.user, contract.user, contract.team, amount, contract.job)
                ws.pay_order = order
                ws.save()

                contract.total_amount += amount
                contract.stone_status = "carry"
                contract.save()

                if amount != ws.amount:
                    margin.refund_amount(contract.team.user, contract.team, contract.job, ws.amount-amount)

                rd.audit_at = now
                rd.save()
                contract.status = "pause"
                contract.save()
            except:
                logger.error(traceback.format_exc())
                txn.rollback()


# 生成按小时工作每天的报表
def weekstone_day_report(body):
    now = utils.local_datetime(utils.now())
    yestorday = utils.timedelta(now, days=-1)
    start = utils.datetime_day_min(yestorday, utc=False)
    end = utils.datetime_day_max(yestorday, utc=False)

    records = ShotRecord.select().where(ShotRecord.shot_at>=start, ShotRecord.shot_at<end)
    period = end.strftime('%Y%m%d')
    dic = {}
    for rd in records:
        weekstone_id = rd.weekstone_id
        if weekstone_id not in dic:
            dic[weekstone_id] = 1
        else:
            dic[weekstone_id] += 1

    for x in dic:
        ws = WeekStone.select().where(WeekStone.id == x).first()
        contract = ws.contract

        report = WeekStoneReport()
        report.contract = contract
        report.user = contract.user
        report.team = contract.team
        report.weekstone = ws
        report.period = period
        report.times = dic[x]
        report.hourly = contract.hourly
        if ws.status == "finish":
            report.status = ws.status
        else:
            report.status = "carry"
        report.save()

