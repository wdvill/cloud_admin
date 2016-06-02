#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import datetime

from common import utils
from decimal import Decimal
from models.contract import Contract, MileStone, WeekStone
from models.user import User
from models.statistics import UserStatistics, UserDiscover
from backend import statistics, misc, widget


def _milestone_report(user, status):
    ms = list()
    if status not in ("carry", "carry_pay", "finish"):
        raise Exception("query status not right") 
    
    if status == "carry":
        # 进行中
        mile_status = ("carry", )
    elif status == "carry_pay":
        # 审核中
        mile_status = ("carry_pay", )
    else:
        # 已入账
        mile_status = ("finish", )
    milestones = MileStone.select().where(MileStone.status << mile_status).order_by(MileStone.start_at)
    for m in milestones:
        ms.append({"start_at": utils.local_datetime_to_str(m.start_at), "job_id": m.contract.job.job_uuid, "job_name": m.contract.job.name, "name": m.name, "amount": m.amount if mile_status != "finish" else m.actual_amount})
    return ms


def _freelancer_report_data(user, status, is_detail=True):
    # 根据合同查询
    qs = (Contract.user == user)
    # 进行中
    if status == "carry":
        # 进行中合同
        qs = (qs & (Contract.status == "carry") & (Contract.stone_status == "carry"))
        # 里程碑进行中
        qs_ms = (qs & (MileStone.status == "carry"))
        #进行中时薪里程碑
        qs_ws = (qs & (WeekStone.status == "carry"))

    # 审核中
    else:
        # 审核中合同
        qs = (qs & (Contract.status << ["carry", "carry_pay"]) & (Contract.stone_status == "carry_pay"))
        # 里程碑审核中
        qs_ms = (qs & (MileStone.status << ["carry_pay", "refuse"]))
        # 审核中里程碑
        qs_ws = (qs & (WeekStone.status == "carry_pay"))

    ms = MileStone.select(MileStone, Contract).join(Contract, on=(MileStone.contract == Contract.id)).where(qs_ms).order_by(MileStone.start_at.desc())
    ws = WeekStone.select(WeekStone, Contract).join(Contract, on=(WeekStone.contract == Contract.id)).where(qs_ws).order_by(WeekStone.start_at.desc())

    ms_list, ws_list = list(), list()
    ms_amount, ws_amount = 0, 0
    for m in ms:
        if is_detail:
            ms_list.append({
                "contract_name": m.contract.name,
                "contract_id": m.contract.uuid,
                "stone_name": m.name,
                "start_at": utils.local_datetime_to_str(m.start_at),
                "amount": m.amount,
            })
        ms_amount += m.amount

    for m in ws:
        # 计算时机需要支付金额
        is_out = False
        if m.shot_times * 10 > m.contract.workload * 6:
            actual_amount = m.contract.workload * m.contract.hourly 
            is_out = True
        else:
            actual_amount = utils.decimal_two(Decimal(m.shot_times * 10 / 6) * m.contract.hourly)

        if is_detail:
            ws_list.append({
                "contract_name": m.contract.name,
                "contract_id": m.contract.uuid,
                "start_at": utils.local_datetime_to_str(m.start_at),
                "end_at": utils.local_datetime_to_str(m.end_at) if m.end_at else "",
                "hourly": m.contract.hourly,
                "workload": m.contract.workload,
                "actual_amount": actual_amount,
                "shot_times": m.shot_times * 10,
                "manual_times": m.manual_times * 10,
                "is_out": is_out,
            })
        ws_amount += actual_amount
    return ms_list, ws_list, (ms_amount + ws_amount)


def freelancer_report(user, params):
    """
    1、开发者统计进行中的工作
    2、开发者统计审核中的工作
    """
    status = params.get("status")
    if status not in ("carry", "carry_pay"):
        return {"error_code": 20611, "msg": "status invalid"}

    if status == "carry":
        ms, ws, amount_carry = _freelancer_report_data(user, "carry")
        _, _, amount_carry_pay = _freelancer_report_data(user, "carry_pay", False) 
    else:
        ms, ws, amount_carry_pay  = _freelancer_report_data(user, "carry_pay")
        _, _, amount_carry= _freelancer_report_data(user, "carry", False) 

    return {"error_code": 0, "msg": "ok", "milestones": ms, "weekstones": ws, 
            "amount_carry": amount_carry, "amount_carry_pay": amount_carry_pay}
    

# 查询推荐的开发者
def freelancer_recommand(user, params):
    key, value = misc.generate_verify_init_data(user, "freelancer_recommend")
    m = misc.misc_get_or_create(key=key, value=value)
    misc_value = utils.loads(m.value)
    # uids 为用户id列表如：[1,2,3]
    uids = misc_value.get("uids")
    if uids:
        users = User.select().where(User.id << uids)
    else:
        users = User.select().where(User.to_dev == True, User.status == "active").limit(3)
    out = list()
    for u in users:
        profile = u.profile.first()
        out.append({
            "id": u.uuid,
            "name": profile.name,
            "avatar": widget.avatar(profile.avatar),
            "title": profile.title,
        })

    return {"error_code": 0, "msg": "ok", "freelancers": out}

def freelancer_statis(user):
    us = UserStatistics.select().where(UserStatistics.user==user).first()
    out = {"year_amount":0, "aver_score":0,
            "recommend":0, "coop_rate_two":0,
            "coop_rate":0, "update_at":"",
            "season_invite":0, "season_reply":0,
            "season_day_reply":0, "season_proposal":0,
            "season_view":0, "season_interview":0,
            "season_hire":0, "views":[]}

    now = utils.now()
    start = utils.datetime_to_day_number(utils.timedelta(now, days=-7))
    end = utils.datetime_to_day_number(utils.timedelta(now, days=-1))

    for x in range(int(start), int(end)+1):
        out["views"].append({"count":0, "period":x})

    if us:
        out.update({"year_amount":us.year_amount, "aver_score":us.aver_score,
                "recommend":us.recommend, "coop_rate_two":0 if not us.coop_success else us.coop_two / us.coop_success,
                "coop_rate":0 if not us.coop else us.coop_success / us.coop, 
                "update_at":utils.datetime_to_str(us.update_at),
                "season_invite":us.season_invite, "season_reply":us.season_reply,
                "season_day_reply":us.season_day_reply, "season_proposal":us.season_proposal,
                "season_view":us.season_view, "season_interview":us.season_interview,
                "season_hire":us.season_hire})
        ud = UserDiscover.select().where(UserDiscover.user==user, 
                            UserDiscover.period >= int(start), 
                            UserDiscover.period <= int(end)).order_by(UserDiscover.update_at.asc())
        for x in ud:
            for y in out["views"]:
                if y["period"] == x.period:
                    y["count"] = x.view_num
                    break
    return {"error_code":0, "msg":"ok", "data":out}
