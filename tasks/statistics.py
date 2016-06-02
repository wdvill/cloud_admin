#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import logging
import datetime
import decimal
import traceback

from peewee import fn
from common import utils, queue
from config.settings import database, user_points_config
from models.contract import Contract, ContractEvaluate, WeekStone
from models.job import Job
from models.proposal import Proposal
from models.team import Team
from models.user import User, UserCategory, UserLanguage, UserPoints
from models.margin import MarginRecord
from models.resume import Employment, Education, Portfolio
from models.statistics import TeamStatistics, UserStatistics, UserDiscover
from models.session import Session


logger = logging.getLogger(__name__)


# 处理评价和评价统计
def evaluate(body):
    ce = ContractEvaluate.select().where(ContractEvaluate.id == body['contract_evaluate_id']).first()
    if not ce:
        return
    if body['role'] == "f":
        # 开发者评价需求者
        score = decimal.Decimal(ce.exchange + ce.cooper + ce.quality + ce.skill + ce.avail + ce.deliver)
    else:
        score = decimal.Decimal(ce.exchange + ce.cooper + ce.quality + ce.skill + ce.punctual)
    score = score.quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_DOWN)
    contract = ce.contract

    if body['role'] == "f":
        ts = TeamStatistics().select().where(TeamStatistics.team == contract.team).first()
        if not ts:
            ts = TeamStatistics()
            ts.user = contract.team.user
            ts.team = contract.team
            ts.eveluate_num = 1
            ts.score = score
            aver_score = decimal.Decimal(ts.score / 6).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_DOWN)
            ts.aver_score = aver_score 
            ts.save()
        else:
            ts.eveluate_num += 1
            ts.score += score
            aver_score = decimal.Decimal(ts.score / ts.eveluate_num / 6).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_DOWN)
            ts.aver_score = aver_score 
            ts.save()
    else:
        us = UserStatistics.select().where(UserStatistics.user == contract.user).first()
        if not us:
            us = UserStatistics()
            us.user = contract.user
            us.eveluate_num = 1
            us.score = score
            aver_score = decimal.Decimal(us.score / 5).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_DOWN)
            us.aver_score = aver_score 
            us.save()
        else:
            us.eveluate_num += 1
            us.score += score
            aver_score = decimal.Decimal(us.score / us.eveluate_num / 5).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_DOWN)
            us.aver_score = aver_score 
            us.save()
    return

# 增加投标
def increase_proposal(body):
    if "user_id" not in body:
        return
    us = UserStatistics.select().where(UserStatistics.user == body["user_id"]).first()
    if not us:
        us = UserStatistics()
        us.user = body["user_id"]
        us.proposal = 1
    else:
        us.proposal += 1
    #now = utils.now()
    #start = utils.timedelta(now, days=-90)
    #count = Proposal.select().where(Proposal.user==user_id,Proposal.ptype=='D',Proposal.create_at.between(start, now)).count()
    #us.season_proposal = count
    #us.update_at = now
    us.save()
    return

# 增加投标成功
def increase_proposal_ok(body):
    if "user_id" not in body:
        return
    us = UserStatistics.select().where(UserStatistics.user == body["user_id"]).first()
    if not us:
        us = UserStatistics()
        us.user = int(body["user_id"])
        us.success = 1
    else:
        us.success += 1
    #now = utils.now()
    #start = utils.timedelta(now, days=-90)
    #count = Proposal.select().where(Proposal.user==user_id,
    #                        Proposal.status=="interview",
    #                        Proposal.update_at.between(start, now)).count()
    #us.update_at = now
    #us.season_interview = count
    us.save()
    return

# 增加被查看
def user_discover_view(body):
    if "uuid" not in body or "user_id" not in body:
        return
    now = utils.now()
    period = utils.datetime_to_day_number(now)
    user = User.select().where(User.uuid==body["uuid"]).first()
    if not user or user.id == int(body["user_id"]):
        return
    ud = UserDiscover.select().where(UserDiscover.user==user, UserDiscover.period==period).first()
    if not ud:
        ud = UserDiscover()
        ud.user = user
        ud.period = utils.datetime_to_day_number(now)
    ud.view_num += 1
    ud.update_at = now
    ud.save()
    return

# 增加被发现
def user_discover(body):
    if "user_ids" not in body or not body["user_ids"]:
        return
    now = utils.now()
    period = utils.datetime_to_day_number(now)
    with database.atomic() as txn:
        dis = UserDiscover.select().where(UserDiscover.user << body["user_ids"], UserDiscover.period == period)
        exist_ids = []
        for ud in dis:
            ud.update_at = now
            ud.discover_num += 1
            ud.save()
            exist_ids.append(ud.user_id)

        not_ids = list(set(body["user_ids"]) - set(exist_ids))
        for user_id in not_ids:
            ud = UserDiscover()
            ud.user = user_id
            ud.period = period
            ud.update_at = now
            ud.discover_num = 1
            ud.save()
    return

# 统计90天内查看数
def calc_user_discover(body):
    now = utils.now()
    start = utils.timedelta(now, days=-90)
    year_start = utils.timedelta(now, days=-365)
    id_start = 0
    while 1:
        users = User.select(User.id).where(User.id>id_start).limit(200)
        if not users:
            break

        for u in users:
            user_id = u.id
            id_start = u.id

            us = UserStatistics.select().where(UserStatistics.user == u.id).first()
            if not us:
                us = UserStatistics()
                us.user = u.id
            count = UserDiscover.select(fn.SUM(UserDiscover.view_num)).where(UserDiscover.user==user_id, UserDiscover.update_at.between(start, now)).scalar()
            us.season_view = count if count else 0

            # 90天内投标
            count = Proposal.select().where(Proposal.user==user_id,Proposal.ptype=='D',Proposal.create_at.between(start, now)).count()
            us.season_proposal = count

            # 90内沟通中
            count = Proposal.select().where(Proposal.user==user_id,
                                    Proposal.status=="interview",
                                    Proposal.update_at.between(start, now)).count()
            us.season_interview = count

            # 90天内被邀请
            count = Proposal.select().where(Proposal.user==user_id,Proposal.ptype=='I',Proposal.create_at.between(start, now)).count()
            us.season_invite = count

            # 90天内被邀请回复
            count = Proposal.select().where(Proposal.user==user_id,
                                    Proposal.ptype=='I',Proposal.status=="interview",
                                    Proposal.update_at.between(start, now)).count()
            us.season_reply = count
            # 90天内被邀请当天回复
            count1 = Proposal.select().where(Proposal.user==user_id,
                                    Proposal.ptype=='I',Proposal.day_reply==True,
                                    Proposal.update_at.between(start, now)).count()
            us.season_day_reply = count1

            # 90天内雇佣
            count = Proposal.select().where(Proposal.user==user_id,
                                    Proposal.status=="hire",
                                    Proposal.update_at.between(start, now)).count()
            us.season_hire = count

            # 一年内收总金额
            year_amount = MarginRecord.select(fn.SUM(MarginRecord.amount)).where(MarginRecord.user==user_id, 
                                        MarginRecord.record_type=="income", MarginRecord.create_at.between(year_start, now)).scalar()
            us.year_amount = year_amount if year_amount else 0
            us.update_at = now
            us.save()



# 项目数统计
def statistics_team_jobs(body):
    if "team_id" not in body:
        return
    team = Team.select().where(Team.id == body["team_id"]).first()
    if not team:
        return
    
    qs = (Job.team == team)
    qs_count = (qs & (Job.status << ["normal", "private", "close"]))
    qs_open = (qs & (Job.status == "normal"))
    jobs_count = Job.select().where(qs_count).count() 
    jobs_open = Job.select().where(qs_open).count()

    ts = TeamStatistics().select().where(TeamStatistics.team == team).first()
    if not ts:
        ts = TeamStatistics()
        ts.user = team.user 
        ts.team = team 
        ts.jobs = 0
        ts.open_jobs = 0

    ts.jobs = jobs_count
    ts.open_jobs = jobs_open
    ts.save()
    return

# 合同开始
def contract_start(body):
    if "contract_id" not in body:
        return
    contract = Contract.select().where(Contract.id == body["contract_id"]).first()
    if not contract:
        return

    team = contract.team
    ts = TeamStatistics().select().where(TeamStatistics.team == team).first()
    if not ts:
        ts = TeamStatistics()
        ts.user = team.user 
        ts.team = team 
    ts.hires += 1
    ts.save() 

    us = UserStatistics.select().where(UserStatistics.user == contract.user).first()
    if not us:
        us = UserStatistics()
        us.user = contract.user
    us.coop += 1
    us.save()
    return
    
# 增加总消费金额
def statistics_team_amount(body):
    if filter(lambda x: x not in body, ["team_id", "amount"]):
        return
    
    team = Team.select().where(Team.id == int(body["team_id"])).first()
    if not team:
        return

    ts = TeamStatistics().select().where(TeamStatistics.team == team).first()
    if not ts:
        ts = TeamStatistics()
        ts.user = team.user 
        ts.team = team
    ts.total_amount += utils.decimal_two(body["amount"]) 
    ts.save()
    return

# 合同结束，计算相关数据
def contract_finish(body):
    if "contract_id" not in body:
        return
    contract = Contract.select().where(Contract.id == body["contract_id"]).first()
    if not contract:
        return

    ts = TeamStatistics().select().where(TeamStatistics.team == contract.team).first()
    if not ts:
        ts = TeamStatistics()
        ts.user = contract.team.user 
        ts.team = contract.team
    ts.total_amount += contract.total_amount
    if contract.hourly > 0:
        time_count = WeekStone.select(fn.sum(WeekStone.shot_times)).where(WeekStone.contract==contract).scalar()
        ts.hours += time_count
    ts.save()

    us = UserStatistics.select().where(UserStatistics.user == contract.user).first()
    if not us:
        us = UserStatistics()
        us.user = contract.user
    us.total_amount += contract.total_amount
    if contract.hourly > 0:
        us.hours += time_count
    us.coop_success += 1

    coop_two_count = Contract.select().where(Contract.user==contract.user, 
                    Contract.status=="finish").group_by(Contract.team).having(fn.count(Contract.team) >= 2).count()
    us.coop_two = coop_two_count
    us.save()

# 清除过期session
def cleanup_session(body):
    now = utils.now()
    qs = Session.delete().where(Session.expire_at <= now)
    qs.execute()


# 合作次数
#def statistics_user_coop(body):
#    if "user_id" not in body:
#        return
#
#    user = User.select().where(User.id == body["user_id"]).first()
#    if not user:
#        return
#
#    qs = (Contract.user == user)
#    qs_coop = (qs & (Contract.status << ["carry", "pause", "finish", "dispute", "service"]))
#    qs_coop_success = (qs & (Contract.status << ["finish", "service"]))
#    
#    coop_count = Contract.select().where(qs_coop).count()
#    coop_success_count = Contract.select().where(qs_coop_success).count()
#    coop_two_count = Contract.select(fn.count(Contract.team)).where(qs).group_by(Contract.team).having(fn.count(Contract.team) >= 2).count()
#
#    us = UserStatistics.select().where(UserStatistics.user == user).first()
#    if not us:
#        us = UserStatistics()
#        us.user = user
#    us.coop = coop_count 
#    us.coop_success = coop_success_count
#    us.coop_two = coop_two_count
#    us.save()
#    return


# 用户资料完整度
def user_completeness(body):
    if filter(lambda x: x not in body, ["user_id", "columns"]):
        return
    user_id = body["user_id"]
    columns = body["columns"]
    user = User.select().where(User.id == user_id).first()
    if not user:
        return
    up = UserPoints.select().where(UserPoints.user == user).first()
    if not up:
        up = UserPoints()
        up.user = user
        up.save()

    profile = user.profile.first()
    points_change  = 0
    for column in columns:
        points = user_points_config.get(column)
        # 新设置加分，去掉后减分, 更改分不变
        if column == "category":
            value = UserCategory.select().where(UserCategory.user == user).count()
        elif column == "avatar":
            value = True if not profile.avatar.startswith("/static/") else False
        elif column == "other_language":
            value = UserLanguage.select().where(UserLanguage.user == user).count() 
        elif column == "employment":
            value = Employment.select().where(Employment.user == user).count()
        elif column == "education":
            value = Education.select().where(Education.user == user).count()
        elif column == "portfolio":
            value = Portfolio.select().where(Portfolio.user == user).count()
        elif column == "email":
            value = getattr(user, column)
        else:
            value = getattr(profile, column) 

        if value:
            if not getattr(up, column):
                setattr(up, column, True)
                points_change += points
        else:
            if getattr(up, column):
                setattr(up, column, False)
                points_change -= points
        # 每次循环完更新字断加分标示
        up.save()
    # 循环完毕更新总分
    profile.completeness += points_change
    profile.save()
    return

# 需求者查看投标详情
def job_view(body):
    if "uuid" not in body or "user_id" not in body:
        return

    job = Job.select().where(Job.job_uuid==body["uuid"]).first()
    if not job or job.user_id != body["user_id"]:
        return
    job.last_view_time = utils.now()
    job.save()

    qs = Proposal.update(is_view=True).where(Proposal.job==job)
    qs.execute()
    return
