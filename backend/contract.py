#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import random
import datetime
import decimal
import logging
import traceback
from common import utils, queue
from config.settings import database
from models.user import User
from models.team import Team
from models.job import Job
from models.question import Question
from models.attachment import Attachment
from models.contract import (Contract, MileStone, MileStoneRecord, 
    ContractRecord, WeekStone, ShotRecord, WeekStoneRecord, ContractEvaluate, 
    OrderBonus,)
from models.margin import Order
from models.feedback import FeedbackContract
from models.statistics import TeamStatistics, UserStatistics
from backend import margin, widget, friend
from peewee import fn


logger = logging.getLogger(__name__)


def freelancer_contract(params):
    user_id = params.get("user_id")
    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    if not user_id or not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20701, "msg": "params not enough"}
    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20702, "msg": "pagesize must less than 100"}

    user = User.select().where(User.uuid == user_id).first()
    if not user:
        return {"error_code": 20703, "msg": "user not exists"}

    contracts = Contract.select().where(Contract.user == user, Contract.status.in_(["carry", "pause", "finish", "dispute", "service"]))
    count = contracts.count()
    contracts = contracts.order_by(Contract.create_at.desc()).paginate(pagenum, pagesize)
    out = []
    for c in contracts:
        if c.job.paymethod == "hour":
            weekstones = WeekStone.select(fn.sum(WeekStone.shot_times)).join(Contract, on=(WeekStone.contract == Contract.id)).where(WeekStone.contract == c, Contract.status.in_(["paid", "carry", "pause", "finish", "dispute", "service"])).scalar()
        else:
            weekstones = None

        out.append({
            "name": c.job.name,
            "paymethod": c.job.paymethod,
            # accept_at 接受拒绝撤消记录时间
            "start_at": utils.local_datetime_to_str(c.accept_at),
            "end_at": utils.local_datetime_to_str(c.actual_end_at),
            "total_amount": c.total_amount,
            "hourly": c.hourly,
            "shot_times": weekstones * 10 if weekstones else 0,
            "status": c.status,
            "evaluate": _contract_evaluate(contract=c),
        })

    return {"error_code": 0, "msg": "ok", "contracts":  out, "count": count, "pagenum": pagenum}


# 合同基本信息列表
def contract_list_basic(user, params):
    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    
    if not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20831, "msg": "parameters not enough"}

    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20832, "msg": "pagesize must less than 100"}

    if user.identify[0] == "f":
        qs = (Contract.user == user)
    else:
        qs = (Contract.team == int(user.identify[1:]))

    qs = (qs & (Contract.status << ["carry", "pause", "finish", "dispute", "service"]))

    contracts = Contract.select().where(qs)
    count = contracts.count()
    contracts = contracts.order_by(Contract.create_at.desc()).paginate(pagenum, pagesize)

    out = []
    for x in contracts:
        out.append({
            "id": x.uuid,
            "name": x.name,
            "amount": x.amount,
            "status": x.status,
            "accept_at": utils.local_datetime_to_str(x.accept_at),
            "actual_end_at": utils.local_datetime_to_str(x.actual_end_at),
            "hourly": x.hourly,
            "workload": x.workload,
            "paymethod": x.job.paymethod,
        })
    return {"error_code": 0, "msg": "ok", "contracts": out, "count": count, "pagenum": pagenum}


# 合同列表
def contract_list(user, params):
    contract_id = params.get("contract_id")
    team_id = params.get("team_id")
    pagesize = params.get("pagesize", "20")
    pagenum = params.get("pagenum", "1")
    status = params.get("status", "")

    if not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20351, "msg": "parameters not enough"}

    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20352, "msg": "pagesize must less than 100"}

    role, uid = user.identify[0], int(user.identify[1:])

    contracts = Contract.select()
    qs = None
    if contract_id:
        qs = (Contract.uuid == contract_id)
    else:
        if (role == "f" and status not in ("paid", "carry_fixed", "carry_hour", "finish", "all", "offer") 
            or role != "f" and status not in ("carry", "carry_pay", "all", "paid", "offer")):
            return {"error_code": 20353, "msg": "status invalid"}

    if role == "f":
        qs = (Contract.user == user) if qs is None else (qs & (Contract.user == user))
        # 待确定合同
        if status == "paid":
            qs = (qs & (Contract.status == "paid"))
        # 固定价格合同
        elif status == "carry_fixed":
            qs = (qs & (Contract.status << ["carry", "pause", "dispute"]) & (Contract.hourly == 0))
        # 时薪合同
        elif status == "carry_hour":
            qs = (qs & (Contract.status << ["carry", "pause", "dispute"]) & (Contract.hourly > 0))
        # 结束合同
        elif status == "finish":
            qs = (qs & (Contract.status << ["finish", "service"]))
        # 全部合同
        elif status == "all":
            # 没有签订成功的offer不展示
            qs = (qs & (Contract.status << ["carry", "pause", "finish", "expire", "dispute", "service"]))
        # 全部offer
        elif status == "offer":
            qs = (qs & (Contract.status != "unpaid"))
    else:
        if team_id:
            team = Team.select().where(Team.user==user, Team.uuid==team_id).first()
            if not team:
                return {"error_code": 20354, "msg": "team_id invalid"}
        else:
            team = int(user.identify[1:])
        
        qs = (Contract.team == team) if qs is None else (qs & (Contract.team == team))
        # 进行中合同
        if status == "carry":
            qs = (qs & (Contract.status << ["carry", "pause", "dispute"]))
        # 待支付合同
        elif status == "carry_pay":
            qs = (qs & (Contract.status == "carry") & (Contract.stone_status == "carry_pay"))
        # 全部合同, offer不展示
        elif status == "all":
            qs = (qs & (Contract.status << ["carry", "pause", "finish", "expire", "dispute", "service"]))
        # 带签约offer
        elif status == "paid":
            qs = (qs & (Contract.status == "paid"))
        # 全部offer
        elif status == "offer":
            qs = (qs & (Contract.status != "unpaid"))

    contracts = Contract.select().where(qs)
    count = contracts.count()
    contracts = contracts.order_by(Contract.create_at.desc()).paginate(pagenum, pagesize)
    out = []
    for x in contracts:
        tmp = dict()
        tmp["id"] = x.uuid
        tmp["name"] = x.name
        tmp["amount"] = x.amount
        tmp["order_id"] = x.order.id if x.order_id else ""
        # 时薪合同填写开始时间，固定价格合同开发者同意offer的时间为开始时间
        tmp["start_at"] = utils.local_datetime_to_str(x.start_at)
        # end_at为合同上的结束时间
        tmp["end_at"] = utils.local_datetime_to_str(x.end_at)
        # accept_at 接受拒绝撤消记录时间
        tmp["accept_at"] = utils.local_datetime_to_str(x.accept_at)
        tmp["expire_at"] = utils.local_datetime_to_str(x.expire_at)
        tmp["actual_end_at"] = utils.local_datetime_to_str(x.actual_end_at)
        tmp["finish_by"] = x.finish_by
        tmp["workload"] = x.workload
        tmp["status"] = x.status
        tmp["stone_status"] = x.stone_status
        tmp["message"] = x.message
        tmp["reason"] = x.reason
        tmp["create_at"] = utils.local_datetime_to_str(x.create_at)
        tmp["amount"] = x.amount
        tmp["total_amount"] = x.total_amount
        tmp["invoice"] = x.invoice
        tmp["hourly"] = x.hourly
        tmp["manual"] = x.manual
        tmp["job"] = {"id": x.job.job_uuid, "name": x.job.name, "paymethod": x.job.paymethod}
        if x.user_evl != 0:
            tmp["is_evaluate"] = True
        else:
            tmp["is_evaluate"] = False

        profile = x.user.profile.first()
        profile_team = x.team.profile.first()
        profile_team_f = x.team.user.profile.first()
        tmp["user"] = {
            "freelancer": {"name": profile.name, "title": profile.title, "id": x.user.uuid,
                "avatar": widget.avatar(profile.avatar), "hourly": profile.hourly},
            "client": {"name": x.team.name, "id": x.team.uuid,
                "avatar": widget.logo(x.team.logo), "name_private": profile_team_f.name}
        }

        is_open_next = False
        if x.job.paymethod == "fixed":
            stones = MileStone.select().where(MileStone.contract == x).order_by(MileStone.term.asc())
            if x.status in ("carry", "pause"):
                is_open_next = True
        else:
            stones = WeekStone.select().where(WeekStone.contract == x).order_by(WeekStone.term.asc())
            if x.status in ("carry", "pause"):
                ws_carry = stones.where(WeekStone.status << ["paid", "carry", "carry_pay", "dispute"]).count()
                if ws_carry == 0:
                    is_open_next = True
        tmp["is_open_next"] = is_open_next

        ms = []
        for m in stones:
            if m.status == "unpaid":
                continue
            t = dict()
            t["id"] = m.id
            t["amount"] = m.amount
            t["status"] = m.status
            t["term"] = m.term
            t["create_at"] = utils.local_datetime_to_str(m.create_at)
            t["end_at"] = utils.local_datetime_to_str(m.end_at)
            if x.job.paymethod == "fixed":
                t["name"] = m.name
                t["actual_amount"] = m.actual_amount
                # 开发者提交审核时间，需求者审核时间
                msr = m.record.order_by(MileStoneRecord.create_at.desc()).first()
                if msr:
                    t["audit_at"] = utils.local_datetime_to_str(msr.audit_at)
                    t["audit_reason"] = msr.reason
                    t["request_at"] = utils.local_datetime_to_str(msr.create_at)
                    t["request_message"] = msr.message
                else:
                    t["audit_at"] = ""
                    t["audit_reason"] = ""
                    t["request_at"] = ""
                    t["request_message"] = ""
            else:
                t["actual_amount"] = m.actual_amount
                t["start_at"] = utils.local_datetime_to_str(m.start_at)
                t["shot_times"] = m.shot_times * 10
                t["end_at"] = utils.local_datetime_to_str(m.end_at)

            ms.append(t)
        tmp["stones"] = ms
        tmp["evaluate"] = _contract_evaluate(contract=x) 
        out.append(tmp)

        if contract_id:
            if x.attachment_id != 0:
                tmp["attachment"] = {"path":widget.attach(x.attachment.path), "name":x.attachment.name, "size":x.attachment.size}
            else:
                tmp["attachment"] = {}
            if x.question_id != 0:
                tmp["question"] = x.question.name
            else:
                tmp["question"] = ""
    return {"error_code": 0, "msg": "ok", "contracts": out, "count": count, "pagenum": pagenum}


# 查询合同评价信息
def _contract_evaluate(contract):
    evaluate = {"user": {}, "team": {}} 
    if contract.user_evl != 0:
        user_evl = ContractEvaluate().select().where(ContractEvaluate.id ==  contract.user_evl).first()
        evaluate["user"] = {
            "exchange":user_evl.exchange, "punctual":user_evl.punctual,
            "cooper":user_evl.cooper, "quality":user_evl.quality,
            "skill":user_evl.skill, "avail":user_evl.avail,
            "deliver":user_evl.deliver, "content":user_evl.content}
    if contract.team_evl != 0:
        team_evl = ContractEvaluate().select().where(ContractEvaluate.id == contract.team_evl).first()
        evaluate["team"] = {
            "exchange":team_evl.exchange, "punctual":team_evl.punctual,
            "cooper":team_evl.cooper, "quality":team_evl.quality,
            "skill":team_evl.skill, "avail":team_evl.avail,
            "deliver":team_evl.deliver, "content":team_evl.content}
    return evaluate


# 发offer
def contract_create(user, params):
    #if user.identify[0] != "c":
    #    return {"error_code":20361, "msg":"identify error"}

    user_id = params.get("user_id", "")
    team_id = int(user.identify[1:])
    job_id = params.get("job_id","")
    name = unicode(params.get("name", ""))
    amount = params.get("amount", "")
    workload = utils.safe_id(params.get("workload"))
    hourly = params.get("hourly", "")
    message = params.get("message", "")
    start_at = params.get("start_at", "")
    end_at = params.get("end_at", "")
    attachment_id = utils.safe_id(params.get("attachment_id", ""))
    milestones = params.get("milestones", "")
    manual = params.get("manual", "")

    if not user_id or not job_id:
        return {"error_code": 20362, "msg": "user_id and job_id required"}
    freelancer = User.select().where(User.uuid == user_id).first()
    if not freelancer or freelancer == user:
        return {"error_code": 20363, "msg": "freelancer required"}
    job = Job.select().where(Job.job_uuid == job_id).first()
    if not job or job.team_id != team_id:
        return {"error_code": 20364, "msg": "job not exists"}

    ct = Contract.select().where(Contract.user == freelancer, 
                        Contract.team == team_id, Contract.job == job, 
                        Contract.status << ("paid", "carry", "pause", "dispute")).first()
    # 已拒绝，过期，撤消的合同可以重新创建一个
    if ct:
        return {"error_code":20365, "msg": "contract exists"}

    now = utils.now()

    if job.paymethod == "hour":
        if milestones != "":
            return {"error_code":20366, "msg": "hour work must has no milestone"}

        hourly = utils.decimal_two(hourly)
        if hourly is None or not 0 <= hourly <= 10000:
            return {"error_code": 20367, "msg": "hourly invalid"}

        if not workload or not 1 <= workload <= 120:
            return {"error_code": 20368, "msg": "workload invalid"}
        total_amount = hourly * workload

        start_at = utils.str_to_date(start_at)
        if start_at is None or start_at < now:
            return {"error_code": 20369, "msg": "start_at invalid"}

        if manual not in ("true", "false"):
            return {"error_code": 203616, "msg": "manual invalid"}
        manual = utils.loads(manual)

    else:
        # 固定价格
        amount = utils.decimal_two(amount)
        if amount is None or amount <= 0:
            return {"error_code": 203610, "msg": "amount invalid"}

        if milestones:
            try:
                tmp_m = utils.loads(milestones)
                if type(tmp_m) != list:
                    raise
                t = 0
                for ms in tmp_m:
                    if "name" not in ms or "amount" not in ms or "end_at" not in ms:
                        raise
                    ms['end_at'] = utils.str_to_date(ms['end_at'])
                    if len(ms['name']) > 20 or utils.decimal_two(str(ms['amount'])) is None or ms['end_at'] is None:
                        raise
                    t += utils.decimal_two(str(ms['amount']))
                if len(tmp_m) > 10:
                    raise
                if t != amount:
                    raise
                milestones = tmp_m
            except Exception, e:
                logger.error(traceback.print_exc())
                return {"error_code": 203611, "msg": "milestone invalid"}
        else:
            milestones = [{"name":name, "amount":amount, "end_at":end_at}]
        total_amount = amount

        end_at = utils.str_to_date(end_at)
        if end_at is None or end_at < now:
            return {"error_code": 203612, "msg": "end_at invalid"}

    # just order
    #user_margin = user.margin.first()
    #if user_margin.margin < total_amount:
    #    return {"error_code":203613, "msg": "has no enough amount", "margin":user_margin.margin}

    if not 5 < len(name) < 50 or not 5 < len(message) < 500:
        return {"error_code": 203614, "msg": "name too long"}

    attach = None
    if attachment_id:
        attach = Attachment.select().where(Attachment.id==attachment_id, Attachment.user == user).first()

    with database.atomic() as txn:
        try:
            contract = Contract()
            contract.name = name
            contract.message = message
            contract.job = job
            contract.team = team_id
            contract.user = freelancer
            contract.amount = total_amount
            if attach:
                contract.attachment = attach

            if job.paymethod == "hour":
                contract.hourly = hourly
                contract.workload = workload
                contract.start_at = start_at
                contract.manual = manual
            else:
                contract.end_at = end_at

            contract.status = "unpaid"
            today = utils.datetime_to_number(utils.now())[2:8]
            invoice = "%s%s" % (today, utils.rand_num())
            while Contract.select(Contract.id).where(Contract.invoice==invoice).first():
                invoice = "%s%s" % (today, utils.rand_num())

            contract.invoice = invoice
            # 将order纪录到对应的里程碑中
            order = margin.process_order(user, contract.team, job, total_amount)
            contract.order = order
            contract.save()

            term = 1
            if job.paymethod == "fixed":
                for ms in milestones:
                    milestone = MileStone()
                    milestone.contract = contract
                    milestone.name = ms['name']
                    milestone.amount = ms['amount']
                    milestone.status = "unpaid"
                    milestone.end_at = ms['end_at']
                    milestone.term = term
                    milestone.order = order
                    milestone.save()
                    term += 1
            else:
                weekstone = WeekStone()
                weekstone.contract = contract
                weekstone.amount = total_amount
                weekstone.status = "unpaid"
                weekstone.term = term
                weekstone.order = order
                weekstone.save()

            ptype = "milestone" if job.paymethod == "fixed" else "weekstone"
            return {"error_code":0, "msg":"ok", "contract_id": contract.uuid, "trade_no": order.trade_no, "ptype": ptype}
        except Exception,e:
            logger.error(traceback.format_exc())
            txn.rollback()
            return {"error_code":203615, "msg":"contract create fail"}

# 操作合同,  处理 接受 拒绝 撤消,状态,暂停
def contract_operate(user, params):
    contract_id = params.get("contract_id", "")
    status = params.get("status", "")
    question_id = params.get("question_id", "")
    reason = params.get("reason", "")
    is_pay = params.get("is_pay", "")

    if not contract_id:
        return {"error_code": 20371, "msg": "contract_id invalid"}

    if status not in ("accept", "refuse", "revoke", "pause", "carry", "finish"):
        return {"error_code": 20372, "msg": "contract stauts invalid"}

    contract = Contract.select().where(Contract.uuid==contract_id).first()
    if not contract:
        return {"error_code": 20373, "msg": "contract not exist"}
    if user.identify[0] == 'f' and contract.user != user:
        return {"error_code": 20374, "msg": "no authority"}
    elif user.identify[0] == 'c' and contract.team.user != user:
        return {"error_code": 20374, "msg": "no authority"}

    if is_pay and is_pay not in ("true", "false"):
        return {"error_code": 203713, "msg": "is_pay invalid"}

    # 开发者
    if contract.user == user:
        if contract.status not in ("paid", "carry") or status not in ("accept", "refuse", "finish"):
            return {"error_code": 20375, "msg": "operate type error"}
        if reason and len(reason) > 400:
            return {"error_code": 20377, "msg": "refuse reason too long"}

        if status == "accept":
            with database.atomic() as txn:
                try:
                    # 接受就开始工作
                    contract.status = "carry"
                    contract.stone_status = "carry"
                    contract.reason = reason
                    if contract.hourly == 0:
                        ms = contract.milestone.where(MileStone.term==1).first()
                        ms.status = "carry"
                        ms.start_at = utils.now()
                        ms.save()
                    else:
                        ms = contract.weekstone.where(WeekStone.term==1).first()
                        ms.status = "carry"
                        now = utils.now()
                        #local_now = utils.local_datetime(now)
                        # 同意时间从昨天晚上12点开始，即当天就开始工作
                        #ms.start_at = utils.datetime_day_min(now + datetime.timedelta(days=1))
                        ms.start_at = utils.datetime_day_min(now)
                        ms.end_at = utils.datetime_day_max(ms.start_at + datetime.timedelta(days=7))
                        ms.save()

                    contract.status = "carry"
                    contract.accept_at = utils.now()
                    contract.save()

                    # 异步发消息合同开始
                    queue.to_queue({"type":"contract_start", "contract_id":contract.id})
                except Exception, e:
                    logger.error(traceback.format_exc())
                    txn.rollback()
        elif status == "refuse":
            # 拒绝要退款
            if not question_id or not Question.select().where(Question.id == question_id, Question.qtype=="contract_refuse").first():
                return {"error_code": 20376, "msg": "refuse question not exists"}
            contract.status = "refuse"
            contract.question = question_id
            contract.reason = reason

            with database.atomic() as txn:
                try:
                    contract.accept_at = utils.now()
                    contract.save()
                    order = margin.refund_amount(contract.team.user, contract.team, contract.job, contract.amount)
                    #send msg to user
                    queue.to_queue({"type": "contract_refuse", "contract_id": contract.id})
                except Exception, e:
                    logger.error(traceback.format_exc())
                    txn.rollback()
                    return {"error_code":20378, "msg":"refuse failed"}
        elif status == "finish" and contract.status in ("carry", "pause", "refuse"):
            # 结束合同
            with database.atomic() as txn:
                try:
                    result = _freelancer_finish_contract(user, contract)
                except:
                    txn.rollback()
                    return {"error_code":203714, "msg":"finish contract fail"}

        return {"error_code":0, "msg":"ok"}

    # 需求者操作
    if status == "revoke":
        if contract.status != "paid":
            return {"error_code": 20379, "msg": "cannot revoke"}

        if not question_id or not Question.select().where(Question.id == question_id, Question.qtype=="contract_revoke").first():
            return {"error_code": 203715, "msg": "revoke question not exists"}
        if reason and len(reason) > 400:
            return {"error_code": 203716, "msg": "revoke reason too long"}

        with database.atomic() as txn:
            try:
                contract.status = "revoke"
                contract.accept_at = utils.now()
                contract.question = question_id
                contract.reason = reason
                contract.save()
                order = margin.refund_amount(user, contract.team, contract.job, contract.amount)
                # send to msg
                queue.to_queue({"type": "contract_revoke", "contract_id": contract.id})
            except Exception,e:
                logger.error(traceback.format_exc())
                txn.rollback()
                return {"error_code":203710, "msg":"revoke failed"}
    elif status == "pause" and contract.status == "carry":
        contract.status = "pause"
        contract.save()

        queue.to_queue({"type":"contract_client_pause", "contract_id":contract.id})
    elif status == "carry" and contract.status == "pause":
        # 开启工作，按小时不同
        if contract.hourly > 0:
            now = utils.now()
            ws = contract.weekstone.order_by(WeekStone.create_at.desc()).first()
            if ws.status != "carry":
                with database.atomic() as txn:
                    try:
                        ws_next = WeekStone()
                        ws_next.contract = contract
                        ws_next.amount = contract.amount
                        ws_next.status = "carry"
                        ws_next.term = ws.term + 1 
                        ws_next.start_at = now 
                        ws_next.end_at = utils.datetime_day_max(now + datetime.timedelta(days=6-now.weekday()))

                        order = margin.freeze_amount(contract.team.user, contract.team, contract.job, contract.amount)
                        ws_next.order = order
                        ws_next.save()
                        # send msg to user
                        queue.to_queue({"type": "contract_client_restart", "contract_id": contract.id})
                    except:
                        txn.rollback()
                        return {"error_code":203717, "msg":"restart contract fail"}

        contract.status = "carry"
        contract.save()

        queue.to_queue({"type":"contract_client_restart", "contract_id":contract.id})
    elif status == "finish" and contract.status in ("carry", "pause", "refuse"):
        # 结束合同
        with database.atomic() as txn:
            try:
                result = _client_finish_contract(user, contract, is_pay)
            except:
                logger.error(traceback.print_exc())
                txn.rollback()
                return {"error_code":203712, "msg":"finish contract fail"}
    else:
        return {"error_code": 203711, "msg": "operate type error"}

    return {"error_code":0, "msg":"ok"}

# 开发者结束合同, user代表开发者
def _freelancer_finish_contract(user, contract):
    if contract.hourly == 0:
        ms = contract.milestone.where(MileStone.status << ("carry", "carry_pay", "refuse")).first()
        ms_paid = contract.milestone.where(MileStone.status == "paid")
        amount = 0
        for x in ms_paid:
            amount += x.amount
            x.status = "cancel"
            x.save()
        if ms:
            ms.status = "cancel"
            ms.save()
            amount += ms.amount

        if amount > 0:
            order = margin.refund_amount(contract.team.user, contract.team, contract.job, amount)
    else:
        ws = contract.weekstone.where(WeekStone.status << ("carry", "carry_pay", "refuse")).first()
        if ws:
            ws.status = "cancel"
            ws.save()

        order = margin.refund_amount(contract.team.user, contract.team, contract.job, contract.amount)

    contract.status = "finish"
    contract.actual_end_at = utils.now()
    contract.finish_by = "user"
    contract.save()
    # send msg to user
    queue.to_queue({"type": "contract_freelancer_finish", "contract_id": contract.id})
    return True

# 需求者结束合同, user代表需求者
def _client_finish_contract(user, contract, is_pay, is_continue="stop"):
    # 固定价格
    if contract.hourly == 0:
        ms = contract.milestone.where(MileStone.status << ("carry", "carry_pay", "refuse")).first()
        ms_paid = contract.milestone.where(MileStone.status == "paid")
        amount = 0
        for x in ms_paid:
            amount += x.amount
            x.status = "cancel"
            x.save()
        if amount > 0:
            order = margin.refund_amount(user, contract.team, contract.job, amount)
        if is_pay == "true":
            if ms:
                order = margin.payment_freelancer(user, contract.user, contract.team, ms.amount, contract.job)
                ms.status = "finish"
                ms.actual_amount = ms.amount
                ms.pay_order = order
                ms.save()
                contract.total_amount += ms.amount
            contract.status = "finish"
            contract.finish_by = "team"
            contract.actual_end_at = utils.now()
            contract.save()
        else:
            if ms:
                ms.status = "dispute"
                ms.save()
                contract.status = "dispute"
                # 争议通知
                queue.to_queue({"type": "contract_dispute_start", "contract_id": contract.id})
            else:
                contract.status = "finish"

            # 争议结束记录时间和身份同正常结束
            contract.finish_by = "team"
            contract.actual_end_at = utils.now()
            contract.save()
        # 结束合同通知 
        queue.to_queue({"type": "contract_client_finish", "contract_id": contract.id})
    # 按小时付费
    else:
        ws = contract.weekstone.where(WeekStone.status << ("carry", "carry_pay")).first()
        if is_pay == "true":
            if ws:
                if ws.shot_times > contract.workload * 6:
                    pay_times = contract.workload * 6
                    amount = contract.amount
                else:
                    pay_times = ws.shot_times
                    amount = utils.decimal_two(ws.shot_times * contract.hourly / 6)
                # 付款开发者
                order = margin.payment_freelancer(user, contract.user, contract.team, amount, contract.job)
                ws.status = "finish"
                ws.pay_order = order
                ws.actual_amount = amount
                ws.save()
                contract.total_amount += amount
                # 多余的退款处理
                order = margin.refund_amount(user, contract.team, contract.job, (ws.amount-amount))
                # 增加需求者雇佣时间
                #queue.to_queue({"type": "statistics_team_hours", "team_id": contract.team_id, "hour": pay_times})
                # 付款通知
                queue.to_queue({"type": "weekstone_client_pass", "weekstone_id": ws.id})
            # 暂停合同
            if is_continue == "pause":
                contract.stone_status = "carry"
                contract.status = "pause"
            # 继续开启下一周
            elif is_continue == "continue":
                contract.stone_status = "carry"
                contract.status = "carry"
            # 结束
            else:
                contract.status = "finish"
                contract.actual_end_at = utils.now()
                contract.finish_by = "team"
                # 结束合同通知
                queue.to_queue({"type": "contract_client_finish", "contract_id": contract.id})
            contract.save()
        else:
            if ws:
                if ws.shot_times == 0:
                    ws.status = "finish"
                    ws.save()
                    contract.status = "finish"
                else:
                    ws.status = "dispute"
                    ws.save()
                    contract.status = "dispute"
                    # 争议通知
                    queue.to_queue({"type": "contract_dispute_start", "contract_id": contract.id})
            # 争议结束记录时间和身份同正常结束
            contract.finish_by = "team"
            contract.actual_end_at = utils.now()
            contract.save()
            # 结束合同通知 
            queue.to_queue({"type": "contract_client_finish", "contract_id": contract.id})
    return True

def _client_weekstone_create(contract):
    if not (contract.status in ("carry", "pause") and contract.stone_status == "carry"):
        raise Exception, "contract status now allow create new weekstone"

    stones = WeekStone.select().where(WeekStone.contract == contract, WeekStone.status << ["paid", "carry", "carry_pay", "dispute"])
    if stones.first():
        raise Exception, "weekstone status now allow create new weekstone"

    qs = (WeekStone.contract == contract)
    qs_paid = (qs & (WeekStone.status != "unpaid"))
    qs_unpaid = (qs & (WeekStone.status == "unpaid"))
    count_paid  = WeekStone.select().where(qs_paid).count()
    ws_next = WeekStone.select().where(qs_unpaid).first()
    if not ws_next:
        ws_next = WeekStone()

    now = utils.now()
    ws_next.contract = contract
    # 现在金额使用合同的金额
    ws_next.amount = contract.amount 
    ws_next.status = "unpaid"
    ws_next.term = count_paid + 1
    ws_next.start_at = utils.datetime_day_min(now) 
    ws_next.end_at = utils.datetime_day_max(ws_next.start_at + datetime.timedelta(days=7))

    order = margin.process_order(contract.team.user, contract.team, contract.job, contract.amount)
    ws_next.order = order
    ws_next.save()
    return ws_next


# 开启下一个里程碑
def weekstone_create(user, params):
    contract_id = params.get("contract_id")
    if not contract_id:
        return {"error_code": 20791, "msg": "contract_id invalid"}

    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20792, "msg": "contract not exists"}

    if int(user.identify[1:]) != contract.team_id:
        return {"error_code": 20795, "msg": "contract user invalid"}

    if not (contract.status in ("carry", "pause") and contract.stone_status == "carry"):
        return {"error_code": 20793, "msg": "contract status not allow"}

    stones = WeekStone.select().where(WeekStone.contract == contract, 
            WeekStone.status << ["paid", "carry", "carry_pay", "dispute"]).first()
    if stones:
        return {"error_code": 20794, "msg": "weekstone status now allow"}

    ws = _client_weekstone_create(contract)
    return {"error_code": 0, "msg": "ok", 
            "contract_id": contract.uuid, 
            "trade_no": ws.order.trade_no, 
            "ptype": "weekstone", "job_id": contract.job.job_uuid}


def milestone_list(user, params):
    """查询里程碑
    需求者可以查询到自己所有的里程碑
    开发者可以查询到正常项目的里程碑
    """
    milestone_id = utils.safe_id(params.get("milestone_id"))
    contract_id = params.get("contract_id", "")
    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20395, "msg": "contract not exists"}

    # 合同拥有的需求者和开发者可以查看合同
    role = (str(user.identify[:1]), int(user.identify[1:]))
    if role[0] == "f" and contract.user != user or role[0] != "f" and contract.team != role[1]:
        return {"error_code": 20396, "msg": "no authority"}

    if role[0] == "f" and contract.status not in ("paid", "carry", "finish", "service", "pause", "dispute"):
        return {"error_code": 20397, "msg": "cannot get milestone"}

    ms = MileStone.select().where(MileStone.contract == contract)
    if milestone_id:
        ms = ms.where(MileStone.id == milestone_id)

    out = []
    for x in ms:
        tmp = dict()
        tmp["id"] = x.id
        tmp["name"] = x.name
        tmp["amount"] = x.amount
        tmp["status"] = x.status
        tmp["term"] = x.term
        tmp["end_at"] = utils.local_datetime_to_str(x.end_at)
        records = x.record.order_by(MileStoneRecord.create_at.desc())
        if records.first() and records[0].audit_at:
            audit_at = utils.local_datetime_to_str(records[0].audit_at)
        else:
            audit_at = ""
        tmp["audit_at"] = audit_at
        rs = []
        if milestone_id:
            for r in records:
                rs.append({
                    "message": r.message,
                    "reason": r.reason,
                    "attachment": {"name": r.attachment.name, 
                                    "path": widget.attach(r.attachment.path)} if r.attachment_id else {},
                    "create_at": utils.local_datetime_to_str(r.create_at),
                    "audit_at": utils.local_datetime_to_str(r.audit_at),
                    "audit_attachment": {"name": r.audit_attachment.name, 
                                        "path": widget.attach(r.audit_attachment.path)} if r.audit_attachment_id else {},
                })
        tmp["records"]= rs
        out.append(tmp)
    return {"error_code": 0, "milestones": out, "msg": "ok"}

# 付款申请页，获取付款数据
def milestone_pay_get(user, params):
    contract_id = params.get("contract_id", "")
    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20431, "msg": "contract not exists"}
    if contract.team.user != user:
        return {"error_code": 20432, "msg": "no authority"}
    # 允许主动释放资金，开发者为提交过，需求者也允许放款
    if contract.stone_status not in("carry", "carry_pay"):
        return {"error_code": 20433, "msg": "contract cannot pay"}
    ms = MileStone.select().where(MileStone.contract==contract, MileStone.status << ("carry", "carry_pay", "refuse")).first()
    if not ms:
        return {"error_code": 20434, "msg": "milestone not exists"}
    records = ms.record.order_by(MileStoneRecord.create_at.desc())
    res = []
    for x in records:
        res.append({"message": x.message,
                    "attachment": widget.attach(x.attachment.path) if x.attachment_id else "",
                    "attachment_name": x.attachment.name if x.attachment_id else "",
                    "create_at": utils.local_datetime_to_str(x.create_at)})

    profile = contract.user.profile.first()
    team = contract.team
    out = {"id": ms.id, "name":ms.name, "amount":ms.amount, "end_at":utils.local_datetime_to_str(contract.end_at),
            "user":{"name":profile.name, "title":profile.title, "avatar": widget.avatar(profile.avatar)},
            "team":{"name":team.name, "avatar":widget.avatar(team.logo)},
            "records":res}
    return {"error_code":0, "msg":"ok", "data":out}


# 计时合同及里程碑信息查询列表
def contract_weekstone_list(user, params):
    qs = ((Contract.hourly > 0) & (Contract.status << ["carry", "pause", "finish", "dispute", "service"]))
    if user.identify[0] == "f":
        qs = (qs & (Contract.user == user))
        ws_status = ["carry", "carry_pay", "finish", "dispute", "service", "cancel"]
    else:
        qs = (qs & (Contract.team == int(user.identify[1:])))
        ws_status = ["carry", "carry_pay", "finish", "dispute", "service", "cancel"]
    
    contracts = Contract.select().where(qs).order_by(Contract.create_at.desc())
    out = []
    for c in contracts:
        tmp = dict()
        tmp["contract_name"] = c.name
        tmp["contract_id"] = c.uuid
        tmp["contract_status"] = c.status
        tmp["hourly"] = c.hourly
        tmp["workload"] = c.workload
        tmp["manual"] = c.manual
        profile = c.user.profile.first()
        tmp["freelancer"] = {"name": profile.name, "id": c.user.uuid}

        ws = WeekStone.select().where(WeekStone.contract == c, WeekStone.status << ws_status).order_by(WeekStone.create_at.asc())
        ws_list = list()
        for w in ws:
            if w.status == "carry":
                amount = 0
            elif w.status in ("carry_pay", "dispute"):
                if w.shot_times > c.workload * 6:
                    pay_times = c.workload * 6
                    amount = c.amount
                else:
                    pay_times = w.shot_times
                    amount = utils.decimal_two(pay_times * c.hourly / 6)
            else:
                amount = w.actual_amount

            # 计时里程碑每周只有一次审核记录
            record = w.record.first()
            ws_list.append({
                "weekstone_id": w.id, 
                "status": w.status,
                "shot_times": w.shot_times * 10,
                "manual_times": w.manual_times * 10,
                "start_at": utils.local_datetime_to_str(w.start_at),
                "end_at": utils.local_datetime_to_str(w.end_at),
                "amount": w.amount, 
                "calculate_amount": amount,
                "create_at": utils.local_datetime_to_str(record.create_at) if record and record.create_at else "",
            })
        if len(ws_list) > 0:
            tmp["weekstones"] = ws_list
            out.append(tmp)
    return {"error_code": 0, "msg": "ok", "contracts": out}

# 计时付款页面获取复关数据
def weekstone_pay_get(user, params): 
    contract_id = params.get("contract_id", "")
    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20771, "msg": "contract not exists"}
    if contract.team.user != user:
        return {"error_code": 20772, "msg": "no authority"}
    if contract.stone_status != "carry_pay":
        return {"error_code": 20773, "msg": "contract cannot pay"}
    ws = WeekStone.select().where(WeekStone.contract == contract, WeekStone.status == "carry_pay").first()
    if not ws:
        return {"error_code": 20774, "msg": "weekstone not exists"}
    
    # 计时里程碑每周只有一次审核记录
    record = ws.record.first()
    freelancer = ws.contract.user.profile.first()
    #if (ws.shot_times + ws.manual_times) > contract.workload * 6:
    if ws.shot_times > contract.workload * 6:
        pay_times = contract.workload * 6
        amount = contract.amount
    else:
        pay_times = ws.shot_times
        amount = utils.decimal_two(pay_times * contract.hourly / 6)
    weekstone = {
            "freelancer": freelancer.name,
            "weekstone_id": ws.id,
            "contract_name": ws.contract.name,
            "contract_id": ws.contract.uuid,
            "hourly": ws.contract.hourly,
            "workload": ws.contract.workload,
            "shot_times": ws.shot_times * 10,
            "start_at": utils.local_datetime_to_str(ws.start_at),
            "end_at": utils.local_datetime_to_str(ws.end_at),
            "amount": ws.amount,
            "manual_times": ws.manual_times,
            "calculate_amount": amount,
            "create_at": utils.local_datetime_to_str(record.create_at),
    }
    return {"error_code":0, "msg":"ok", "weekstone": weekstone}


def milestone_create(user, params):
    contract_id = params.get("contract_id", "")
    milestones = params.get("milestones")
    if not contract_id or not milestones:
        return {"error_code": 20391, "msg": "parameters invalid"}

    if milestones:
        try:
            tmp_m = utils.loads(milestones)
            if type(tmp_m) != list:
                raise
            total_amount = 0
            for ms in tmp_m:
                if "name" not in ms or "amount" not in ms or "end_at" not in ms:
                    raise
                ms['end_at'] = utils.str_to_date(ms['end_at'])
                if len(ms['name']) > 20 or utils.decimal_two(str(ms['amount'])) is None or ms['end_at'] is None:
                    raise
                total_amount += utils.decimal_two(str(ms['amount']))
            milestones = tmp_m
        except:
            logger.error(traceback.format_exc())
            return {"error_code": 20392, "msg": "milestone invalid"}

    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20393, "msg": "contract not exists"}

    if contract.team.user != user:
        return {"error_code": 20394, "msg": "no authority"}

    if contract.status not in ("paid", "carry", "pause"):
        return {"error_code": 20395, "msg": "cannot create milestone"}

    if contract.job.paymethod != "fixed":
        return {"error_code": 20396, "msg": "contract is not fixed"}

    with database.atomic() as txn:
        try:
            order = margin.process_order(user, contract.team, contract.job, total_amount)
            # 统计已存在的里程碑数量
            term = MileStone.select().where(MileStone.contract == contract).count()

            for m in milestones: 
                term += 1 
                ms = MileStone()
                ms.contract = contract
                ms.name = m["name"] 
                ms.amount = m["amount"]
                ms.status = "unpaid"
                ms.order = order
                ms.term = term 
                ms.end_at = m["end_at"]
                ms.save()

            # TODO 额外批量增加里程碑如何发送通知
            # send msg to user
            # queue.to_queue({"type": "milestone_create", "milestone_id": ms.id})
            return {"error_code": 0, "msg": "ok", "contract_id": contract.uuid, "trade_no": order.trade_no}
        except:
            logger.error(traceback.format_exc())
            txn.rollback()
            return {"error_code": 20398, "msg": "create fail"}


def milestone_audit(user, params):
    attachment_id = params.get("attachment_id")
    message = params.get("message", "")
    milestone_id = utils.safe_id(params.get("milestone_id"))
    if not milestone_id:
        return {"error_code": 20399, "msg": "milestone_id invalid"}

    milestone = MileStone.select().where(MileStone.id == milestone_id).first()
    if not milestone:
        return {"error_code": 203910, "msg": "milestone not exists"}

    if milestone.status not in ("carry", "carry_pay", "refuse"):
        return {"error_code": 203917, "msg": "milestone status not allow audit"}

    if attachment_id:
        attachment = Attachment.select().where(Attachment.id == attachment_id).first()
        if not attachment or attachment.user != user:
            return {"error_code": 203912, "msg": "attachment_id invalid"}

    # 开发者 提交审核
    if user.identify[0] == "f":
        if not message or len(message) > 500:
            return {"error_code": 203911, "msg": "message invalid"}
        with database.atomic() as txn:
            try:
                record = MileStoneRecord()
                record.milestone = milestone
                record.message = message
                if attachment_id:
                    record.attachment = attachment_id
                record.save()
                # 更新里程碑状态未提交审核
                milestone.status = "carry_pay"
                milestone.save()

                # 标记合同存在待付款里程碑
                contract = milestone.contract
                contract.stone_status = "carry_pay"
                contract.save()
                # send msg to user
                queue.to_queue({"type": "milestone_freelancer_audit", "milestone_id": milestone.id})
                return {"error_code": 0, "msg": "ok"}
            except:
                txn.rollback()
                return {"error_code": 203915, "msg": "audit fail"}
    # 需求者
    else:
        is_agree = params.get("is_agree")
        is_stop = params.get("is_stop", "false")
        if is_agree not in ("accept", "refuse", "release") or is_stop not in ("true", "false"):
            return {"error_code": 203916, "msg": "is_agree or is_stop invalid"}

        with database.atomic() as txn:
            try:
                record = MileStoneRecord.select().where(MileStoneRecord.milestone == milestone).order_by(MileStoneRecord.create_at.desc()).first()

                # 审核通过
                if is_agree in ("accept", "release"):
                    # 开发者未提交审核，需求者也允许主动释放资金
                    if not record:
                        record = MileStoneRecord()
                        record.milestone = milestone

                    record.audit_at = utils.now()
                    record.save()

                    order = margin.payment_freelancer(
                        user=user, freelancer=milestone.contract.user,
                        team=milestone.contract.team, amount=milestone.amount,
                        job=milestone.contract.job)

                    milestone.pay_order = order
                    milestone.status = "finish"
                    milestone.actual_amount = milestone.amount
                    milestone.save()
                    # 自动开启下一个里程碑
                    ms = MileStone.select().where(MileStone.contract == milestone.contract).order_by(MileStone.term.asc())
                    for m in ms:
                        if m.status == "paid":
                            m.status = "carry"
                            m.start_at = utils.now()
                            m.save()
                            break
                   
                    # send msg to user
                    queue.to_queue({"type": "milestone_client_pass", "milestone_id": milestone.id})

                    # 标记合同不存在待付款里程碑
                    contract = milestone.contract
                    contract.stone_status = "carry"
                    contract.total_amount += milestone.amount
                    contract.save()
                    # 结束合同
                    if is_stop == "true":
                        _client_finish_contract(user, contract, "true")
                # 审核不通过
                else:
                    if not message or len(message) > 500:
                        return {"error_code": 203911, "msg": "message invalid"}
                    if not record:
                        return {"error_code": 203918, "msg": "milestone record not exists"}
                    record.reason = message
                    if attachment_id:
                        record.audit_attachment = attachment_id
                    record.audit_at = utils.now()
                    record.save()
                    # 不同意提交
                    milestone.status = "refuse"
                    milestone.save()

                    # 标记合同不存在待付款里程碑
                    contract = milestone.contract
                    contract.stone_status = "carry"
                    contract.save()
                    # send msg to user
                    queue.to_queue({"type": "milestone_client_unpass", "milestone_id": milestone.id})
                return {"error_code": 0, "msg": "ok"}
            except:
                logger.error(traceback.format_exc())
                txn.rollback()
                return {"error_code": 201916, "msg": "audit fail"}

def weekstone_list(user, params):
    contract_id = params.get("contract_id", "")

    if not contract_id:
        return {"error_code":20751, "msg":"params invalid"}

    contract = Contract.select().where(Contract.uuid==contract_id).first()
    if not contract:
        return {"error_code":20752, "msg":"contract not exists"}
    if contract.hourly == 0 or contract.status not in ("carry", "pause"):
        return {"error_code":20753, "msg":"contract cannot get shot"}

    stone = WeekStone.select().where(WeekStone.contract == contract)
    if not stone:
        return {"error_code":20754, "msg":"contract has no weekstone"}
    out = []
    for x in stone:
        out.append({"id":x.id, "start_at":utils.datetime_to_str(x.start_at),
                    "end_at":utils.datetime_to_str(x.end_at), "shot_times":x.shot_times,
                    "actual_amount":x.actual_amount, "status":x.status,
                    "manual_times":x.manual_times})
    return {"error_code":0, "msg":"ok", "weekstone":out}

# 什么身份都可操作
def shot_create(user, params):
    #if user.identify[0] != "f":
    #    return {"error_code":20401, "msg":"no authority"}
    name = params.get("name", "")
    shot_time = params.get("shot_time", "")
    description = params.get("description", "")
    activity = params.get("activity", "")
    keyboard = params.get("keyboard", "")
    mouse = params.get("mouse", "")
    contract_id = params.get("contract_id", "")
    attachment_id = params.get("attachment_id", "")
    is_auto = params.get("is_auto", "1")

    if not shot_time or not activity or not keyboard or not mouse or not contract_id:
        return {"error_code":20402, "msg":"params invlaid"}

    if is_auto == "1" and not name or name and len(name) > 30 or len(description) > 500:
        return {"error_code":20403, "msg":"name or description too long"}
    if not activity.isdigit() or not keyboard.isdigit() or not mouse.isdigit():
        return {"error_code":20404, "msg":"parameter must be integer"}

    activity, keyboard, mouse = int(activity), int(keyboard), int(mouse)
    if not 0 <= activity <= 100 or keyboard < 0 or mouse < 0 or is_auto not in ("0", "1"):
        return {"error_code":20405, "msg":"parameter area error"}

    #shot_at = utils.str_to_datetime(shot_time, utc=False)
    if is_auto== "0":
        shot_at = utils.str_to_datetime(shot_time)
        shot_at += datetime.timedelta(seconds=random.randint(1,120))
    else:
        shot_at = utils.str_to_datetime(shot_time, utc=False)
    if not shot_at:
        return {"error_code":204010, "msg":"parameter area error"}
    
    contract = Contract.select().where(Contract.uuid==contract_id).first()
    if not contract:
        return {"error_code":20406, "msg":"contract not exists"}
    if contract.hourly == 0 or contract.status != "carry":
        return {"error_code":20407, "msg":"contract cannot sutmit shot"}

    if not contract.manual and is_auto == 0:
        return {"error_code":204015, "msg":"contract not allowed manual shot"}

    stone = contract.weekstone.where(WeekStone.status == "carry").first()
    if not stone:
        return {"error_code":20408, "msg":"workdaily not exists"}

    if not stone.start_at <= shot_at <= stone.end_at:
        return {"error_code":204011, "msg":"shot_time error"}

    shot_start, shot_end = utils.datetime_interval(shot_at)
    record = ShotRecord.select().where(ShotRecord.weekstone==stone, ShotRecord.shot_at.between(shot_start, shot_end)).first()
    if record:
        return {"error_code":204012, "msg":"shot exists"}

    if is_auto == "1":
        if not attachment_id:
            return {"error_code":20402, "msg":"params invlaid"}
        attach = Attachment.select().where(Attachment.id==attachment_id).first()
        if not attach or attach.atype != "shot" or attach.user != user:
            return {"error_code":20409, "msg":"attachment not exists"}
    else:
        attach = None

    #if stone.shot_times >= contract.workload * 6:
    #    return {"error_code":204013, "msg":"shot cannot large than workload"}

    with database.atomic() as txn:
        try:
            record = ShotRecord()
            record.weekstone = stone
            record.name = name
            record.shot_at = shot_at
            record.hour = shot_at.hour
            record.activity = activity
            record.keyboard = keyboard
            record.mouse = mouse
            record.description = description
            if is_auto == "1":
                record.is_auto = True
                record.attachment = attach
            else:
                stone.manual_times += 1
            record.user = contract.user
            record.team = contract.team
            record.save()

            stone.shot_times += 1
            stone.save()
            # 每周开启工作通知
            if stone.shot_times == 1:
                queue.to_queue({"type": "weekstone_shot_first", "weekstone_id": stone.id})
            # 开发者第一次上传发送通知
            f_count = ShotRecord.select().where(ShotRecord.user == contract.user).count()
            if f_count == 1:
                queue.to_queue({"type": "freelancer_shot_first", "shot_id": record.id})
        except Exception,e:
            logger.error(traceback.format_exc())
            return {"error_code":204014, "msg":"shot record fail"}
    return {"error_code":0, "msg":"ok"}


# 查询单个截屏记录详情
def _shot_one(user, params):
    contract_id = params.get("contract_id", "")
    shot_id = utils.safe_id(params.get("shot_id"))
    if not shot_id or not contract_id:
        return {"error_code": 20891, "msg": "shot_id invalid"}

    qs = (Contract.uuid == contract_id)
    qs_record = (qs & (ShotRecord.id == shot_id))
    qs_up = (qs & (ShotRecord.id == (shot_id - 1)))
    qs_down = (qs & (ShotRecord.id == (shot_id + 1)))

    shot_record = ShotRecord.select().join(
        WeekStone, on=(ShotRecord.weekstone == WeekStone.id)
    ).join(
        Contract, on=(WeekStone.contract == Contract.id)
    )

    record = shot_record.where(qs_record).first()
    if not record:
        return {"error_code": 20892, "msg": "record not exists"}

    contract = record.weekstone.contract
    role = str(user.identify[0]), int(user.identify[1:])
    if not (role[0] == "f" and contract.user == user or role[0] != "f" and contract.team_id == role[1]):
        return {"error_code": 20894, "msg": "permision invalid"}

    # 上一条
    if shot_id - 1 <= 0:
        is_page_up = False
    else:
        is_page_up = bool(shot_record.where(qs_up).count())
    # 下一条 
    is_page_down = bool(shot_record.where(qs_down).count())

    profile = contract.user.profile.first()
    shot = {
        "id": record.id, "name": record.name, "description": record.description,
        "shot_at": utils.local_datetime_to_str(record.shot_at),
        "hour": utils.local_datetime(record.shot_at).hour,
        "activity": record.activity, "keyboard": record.keyboard,
        "is_auto": record.is_auto, "mouse":record.mouse,
        "attachment": widget.attach(record.attachment.path if record.attachment_id else ""),
        "freelancer": {"name": profile.name, "avatar": widget.avatar(profile.avatar)},
        "is_page_up": is_page_up, "is_page_down": is_page_down,
    }

    return {"error_code": 0, "msg": "ok", "shot": shot}


def shot_list(user, params):
    # 如果传shot_id 直接掉用查询单个方法返回
    shot_id = utils.safe_id(params.get("shot_id"))
    if shot_id:
        return _shot_one(user, params) 

    contract_id = params.get("contract_id", "")
    shot_at = utils.str_to_date(params.get("shot_time"), utc=False)
    t = params.get("t", "")

    if not contract_id or not shot_at:
        return {"error_code":20411, "msg":"parameter invalid"}
    contract = Contract.select().where(Contract.uuid==contract_id).first()
    if not contract:
        return {"error_code":20412, "msg":"contract not exists"}
    if contract.hourly == 0 or contract.status in ("paid", "cancel"):
        return {"error_code":20413, "msg":"contract cannot get screenshot"}

    role, uid = user.identify[0], int(user.identify[1:])
    if role != "f" and uid != contract.team_id or role == "f" and uid != contract.user_id:
        #if role == "c" and uid != contract.team_id or role == "f" and uid != contract.user_id:
        return {"error_code":20414, "msg":"no authority"}

    ws = contract.weekstone.where(WeekStone.status << ["carry", "refuse", "carry_pay", "dispute", "finish", "service"]).first()

    if t == "last":
        records = ShotRecord.select().join(WeekStone).where(ShotRecord.weekstone == ws).order_by(ShotRecord.shot_at.desc()).limit(1)
    else:
        start, end = utils.datetime_day_min(shot_at), utils.datetime_day_max(shot_at)
        records = ShotRecord.select().join(WeekStone).where(ShotRecord.weekstone == ws, ShotRecord.shot_at.between(start, end))
    out = []
    for x in records:
        out.append({
            "id":x.id, "name":x.name, "description":x.description,
            "shot_at":utils.local_datetime_to_str(x.shot_at),
            "hour":utils.local_datetime(x.shot_at).hour,
            "activity":x.activity, "keyboard":x.keyboard, "is_auto":x.is_auto,
            "mouse":x.mouse, 
            "attachment": widget.attach(x.attachment.path if x.attachment_id else "")})

    return {"error_code":0, "msg":"ok", "shots":out}

# 什么身份都可操作
def shot_delete(user, params):
    shot_ids = params.get("shot_ids")
    if not shot_ids:
        return {"error_code":20421, "msg":"params invalid"}

    arr = shot_ids.split(",")
    arr = [int(x) for x in arr if x.isdigit()]
    if not arr:
        return {"error_code":20421, "msg":"params invalid"}

    records = ShotRecord.select().where(ShotRecord.id << arr)

    # TODO 将附件也删除
    with database.atomic() as txn:
        try:
            for rd in records:
                stone = rd.weekstone
                if rd.user != user or stone.status not in ("refuse", "carry", "carry_pay"):
                    continue

                if not rd.is_auto:
                    stone.manual_times -= 1
                rd.delete_instance()

                if stone.status == "refuse":
                    stone.status = "carry_pay"
                    ws_record = WeekStoneRecord()
                    ws_record.weekstone = stone
                    ws_record.save()
                stone.shot_times -= 1
                stone.save()
        except:
            logger.error(traceback.format_exc())
            return {"error_code":20424, "msg":"shot delete fail"}
    return {"error_code":0, "msg":"ok"}

def shot_update(user, params):
    shot_ids = params.get("shot_ids", "")
    name = unicode(params.get("name", ""))
    if not name or len(name) > 30 or not shot_ids:
        return {"error_code":20781, "msg":"params invalid or name length large than 30"}

    arr = shot_ids.split(",")
    arr = [int(x) for x in arr if x.isdigit()]
    record = ShotRecord.select().where(ShotRecord.user==user, ShotRecord.id==arr[0]).first()
    if not record or record.weekstone.status not in ("carry", "carry_pay"):
        return {"error_code":20782, "msg":"record not exist or cannot update"}

    query = ShotRecord.update(description=name).where(ShotRecord.weekstone == record.weekstone, ShotRecord.id << arr)
    num = query.execute()
    if num:
        return {"error_code":0, "msg":"ok"}
    return {"error_code":20783, "msg":"record not exist"}


# 查询等待支付合同的固定价格还是时薪 
def get_contract_job(uuid):
    contract = Contract.select().where(Contract.uuid==uuid).first()
    if not contract:
        return False
    # 时薪带支付
    if contract.hourly > 0 and contract.stone_status == "carry_pay":
        return 'hour'
    # 固定价格带支付
    if contract.hourly == 0 and contract.status == "carry":
        return 'fixed'
    return False

def weekstone_audit(user, params):
    is_agree = params.get("is_agree", "")
    status = params.get("status", "")
    weekstone_id = utils.safe_id(params.get("weekstone_id"))
    
    if is_agree not in ("accept", "refuse"):
        return {"error_code": 20781, "msg": "is_agree invalid"}

    if is_agree and status not in ("pause", "continue", "stop"):
        return {"error_code": 20782, "msg": "status invalid"}

    stone = WeekStone.select().where(WeekStone.id==weekstone_id).first()
    if not stone:
        return {"error_code": 20783, "msg": "weekstone not exists"}
    if stone.status != "carry_pay":
        return {"error_code": 20784, "msg": "contract cannot pay"}

    contract = stone.contract
    if contract.status != "carry":
        return {"error_code": 20785, "msg": "contract cannot pay"}
    if int(user.identify[1:]) != contract.team_id:
        return {"error_code": 20786, "msg": "no authority"}

    record = stone.record.first()

    with database.atomic() as txn:
        try:
            now = utils.now()
            # 记录审核时间
            record.audit_at = now
            record.save()

            # 审核同意 
            if is_agree == "accept": 
                # pause: 付款，保留合同，不开启下一周
                # continue: 付款，保留合同，开启下一周
                # stop: 付款，结束合同
                result = _client_finish_contract(contract.team.user, contract, is_pay="true", is_continue=status)
                if status == "continue":
                    ws = _client_weekstone_create(contract)
                    return {"error_code": 0, "msg": "ok", "contract_id": ws.contract.uuid, "trade_no": ws.order.trade_no}
            # 拒绝
            else:
                result = _client_finish_contract(contract.team.user, contract, is_pay="false")
            return {"error_code": 0, "msg": "ok"}
        except:
            logger.error(traceback.format_exc())
            txn.rollback()
            return {"error_code": 20787, "msg": "trade fail"}


def contract_freelancers(user, params):
    """ 雇佣的人 """
    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    if not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20621, "msg": "params not enough"}

    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20622, "msg": "pagesize must less than 100"}

    qs = ((Contract.team == int(user.identify[1:])) & 
        (Contract.status << ["carry", "pause", "finish", "dispute", "service"]))

    u_list = list()
    contracts = Contract.select().where(qs)
    users = Contract.select(Contract.user).where(qs).group_by(Contract.user)
    count = users.count()
    users = users.paginate(pagenum, pagesize)
    for u in users:
        # 查询改开发者的合同信息
        c_list = list()
        qs_c = (qs & (Contract.user == u.user)) 
        cs = Contract.select(Contract.name, Contract.uuid, Contract.accept_at).where(qs_c).order_by(Contract.accept_at.desc()) 
        for c in cs:
            c_list.append({
                "name": c.name,
                "id": c.uuid,
            })
        
        # 查询正在雇佣的情况 
        qs_hire = (qs_c & (Contract.status << ["carry", "pause"]))
        hiring_count = Contract.select(Contract.id).where(qs_hire).count()
        # 最后一次签订的合同
        cs_last = cs.first()
        profile = u.user.profile.first()

        u_list.append({
            "user_id": u.user.uuid,
            "name": profile.name,
            "avatar": widget.avatar(profile.avatar),
            "overview": profile.overview,
            "hiring": True if hiring_count > 0 else False, 
            "last_hire_time": utils.local_datetime_to_str(cs_last.accept_at) if cs_last else "", 
            "contracts": c_list,
        })
        
    return {"error_code": 0, "msg": "ok", "freelancers": u_list, "pagenum": pagenum, "count": count}

# 合同评价
def contract_evaluate(user, params):
    question_id = utils.safe_id(params.get("question_id"))
    score = utils.safe_id(params.get("score"))

    exchange = utils.safe_id(params.get("exchange"))
    punctual = utils.safe_id(params.get("punctual"))
    cooper = utils.safe_id(params.get("cooper"))
    quality = utils.safe_id(params.get("quality"))
    skill = utils.safe_id(params.get("skill"))

    avail = utils.safe_id(params.get("avail"))
    deliver = utils.safe_id(params.get("deliver"))

    content = params.get("content", "")
    contract_id = params.get("contract_id", "")

    role, uid = user.identify[0], int(user.identify[1:])
    for x in (question_id, score, exchange, cooper, quality, skill, content, contract_id):
        if not x:
            return {"error_code":20731, "msg":"params invalid"}
    if role == "f":
        if not avail or not deliver:
            return {"error_code":20731, "msg":"params invalid"}
        val = (exchange, cooper, quality, skill, avail, deliver)
    else:
        if not punctual:
            return {"error_code":20731, "msg":"params invalid"}
        val = (exchange, punctual, cooper, quality, skill)
    for y in val:
        if not 1<= y <= 5:
            return {"error_code":20732, "msg":"evaluate between 1-5"}
    if not 1 <= score <= 10 or len(content) > 500:
        return {"error_code":20733, "msg":"recommand between 1-10"}
    contract = Contract.select().where(Contract.uuid==contract_id).first()
    if not contract or role == "f" and contract.user_id != uid or role == "c" and contract.team_id != uid:
        return {"error_code":20734, "msg":"contract not exists"}

    if contract.status not in ("finish", "dispute", "service"):
        return {"error_code":20735, "msg":"contract not finish"}

    if role == "f" and contract.user_evl != 0 or role == "c" and contract.team_evl != 0:
        return {"error_code":20736, "msg":"contract already evaluate"}

    if role == "f":
        qtype = "contract_finish_f"
    else:
        qtype = "contract_finish_c"
    question = Question.select().where(Question.id == question_id, Question.qtype==qtype).first()
    if not question:
        return {"error_code":20737, "msg":"question not exists"}

    with database.atomic() as txn:
        try:
            ce = ContractEvaluate()
            ce.exchange = exchange
            ce.cooper = cooper
            ce.quality = quality
            ce.skill = skill
            ce.content = content
            ce.contract = contract
            ce.identify = role
            if role == "c":
                ce.punctual = punctual
            else:
                ce.avail = avail
                ce.deliver = deliver
            ce.save()
            if role == "f":
                contract.user_evl = ce.id
            else:
                contract.team_evl = ce.id
            contract.save()

            fc = FeedbackContract()
            fc.contract = contract
            fc.question = question
            fc.user = user
            if role == "c":
                fc.team = uid
            fc.score = score
            fc.save()

            queue.to_queue({"type": "contract_evaluate", "role":role, "contract_evaluate_id": ce.id})
        except:
            txn.rollback()
            return {"error_code":20738, "msg":"evaluate fail"}
    return {"error_code":0, "msg":"ok"}

# 获取工作时长
def get_weekstone_time(user, params):
    contract_id = params.get("contract_id", "")

    if not contract_id:
        return {"error_code":20761, "msg":"parameter invalid"}
    contract = Contract.select().where(Contract.uuid==contract_id, Contract.hourly>0).first()
    if not contract:
        return {"error_code":20762, "msg":"contract not exists"}
    if contract.hourly == 0 or contract.status in ("paid", "cancel"):
        return {"error_code":20763, "msg":"contract cannot get time"}

    role, uid = user.identify[0], int(user.identify[1:])
    if uid not in (contract.team_id, contract.user_id) and user.id not in (contract.team_id, contract.user_id):
        #if role == "c" and uid != contract.team_id or role == "f" and uid != contract.user_id:
        return {"error_code":20764, "msg":"no authority"}

    ws = contract.weekstone.where(WeekStone.status << ["carry", "refuse", "carry_pay"]).first()

    shot_at = utils.now()
    start, end = utils.datetime_day_min(shot_at), utils.datetime_day_max(shot_at)
    count = ShotRecord.select().where(ShotRecord.weekstone == ws, ShotRecord.shot_at.between(start, end)).count()

    return {"error_code":0, "msg":"ok", "today":count, "total_time":ws.shot_times}

# desktop专用
def get_desktop_weekstone(user, params):
    contract_id = params.get("contract_id", "")

    if contract_id:
        contracts = Contract.select().where(Contract.uuid==contract_id, Contract.hourly>0, Contract.status=="carry", Contract.stone_status=="carry")
    else:
        contracts = Contract.select().where(Contract.user==user, Contract.hourly>0, Contract.status=="carry", Contract.stone_status=="carry")
    out = []
    for x in contracts:
        ws = x.weekstone.where(WeekStone.status=="carry").first()
        if not ws:
            continue
        out.append({"name":x.name, "id":x.uuid, "team":{"name":x.team.name, "logo":widget.logo(x.team.logo)}, 
                "weekstone":{"start_at":utils.datetime_to_str(ws.start_at),
                "end_at":utils.datetime_to_str(ws.end_at), "shot_times":ws.shot_times,
                "manual_times":ws.manual_times, "id":ws.id}})
    return {"error_code":0, "msg":"ok", "data":out}

def contract_bonus_order(user, params):
    """ 转账生成订单"""
    contract_id = params.get("contract_id")
    amount = utils.decimal_two(params.get("amount"))
    freelancer_id = params.get("freelancer_id")
    description = params.get("description", "")
    if not amount or not freelancer_id or not contract_id:
        return {"error_code": 20801, "msg": "params invalid"}

    if description and len(description) > 200:
        return {"error_code": 20806, "msg": "description invalid"}

    freelancer = User.select().where(User.uuid == freelancer_id).first()
    if not freelancer:
        return {"error_code": 20802, "msg": "freelancer not exists"}

    if freelancer.id == user.id:
        return {"error_code": 20803, "msg": "freelancer not allow self"}

    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20804, "msg": "contract not exists"}

    with database.atomic() as txn:
        try:
            order_c, order_f = margin.transfer_order(
                user=user, 
                team=int(user.identify[1:]),
                freelancer=freelancer,
                amount=amount
            )
            
            bonus = OrderBonus()
            bonus.order = order_c
            bonus.user = user
            bonus.team = int(user.identify[1:]) 
            bonus.freelancer = freelancer
            bonus.amount = order_c.amount 
            bonus.fee = order_c.fee
            bonus.pay_order = order_f
            bonus.contract = contract
            bonus.description = description
            bonus.status = "process"
            bonus.save()
            # 使用需求者的付款交易号回调处理
            return {"error_code": 0, "msg": "ok", "contract_id": contract.uuid, "trade_no": order_c.trade_no}
        except:
            logger.error(traceback.print_exc())
            txn.rollback()
            return {"error_code": 20805, "msg": "trade fail"}


def contract_bonus_query(user, params):
    trade_no = params.get("trade_no")
    if not trade_no:
        return {"error_code": 20821, "msg": "trade_no invalid"}

    order_c = Order.select().where(Order.trade_no == trade_no).first()
    if not order_c:
        return {"error_code": 20822, "msg": "trade_no not exists"}

    bonus = OrderBonus.select().where(OrderBonus.order == order_c).first()
    if not bonus:
        return {"error_code": 20823, "msg": "bonus record not exists"}
    out = {
        "contract_name": bonus.contract.name,
        "description": bonus.description, 
        "amount": (bonus.amount + bonus.fee),
    } 
    return {"error_code": 0, "msg": "ok", "bonus": out}
 

# 临时测试使用手动提审
def test_contract_weekstone_audit(params):
    now = utils.now()

    contract_id = params.get("contract_id")
    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract or contract.status != "carry":
        return {"message": "合同状态不合法或者合同不存在:%s" % contract.status if contract else ""}
     
    weekstones = WeekStone.select().where(WeekStone.contract == contract)
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
                return {"message": "合同提审成功"}
            except:
                logger.error(traceback.format_exc())
                txn.rollback()
                return {"message": "合同提审成功"}
    return {"message": "没有找到合适的时薪周"}

