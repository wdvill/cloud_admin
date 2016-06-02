#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import datetime
from models.statistics import TeamStatistics
from models.team import Team 
from models.contract import WeekStoneReport

def _team_statistics(user, team):
    ts = TeamStatistics.select().where(TeamStatistics.user == user, 
            TeamStatistics.team == team).first()
    if not ts:
        return dict() 
    info = dict()
    info["eveluate_num"] = ts.eveluate_num
    info["total_amount"] = ts.total_amount
    info["score"] = ts.score
    info["hours"] = ts.hour
    info["jobs"] = ts.jobs
    info["hires"] = ts.hires
    info["open_jobs"] = ts.open_jobs
    return info


def user_statistics(params):
    team_id = params.get("team_id")
    if not team_id:
        return {"error_code": 20491, "msg": "team_id invalid"} 

    team = Team.select().where(Team.uuid == team_id).first()
    if not team:
        return {"error_code": 20492, "msg": "team not exists"}
    
    info = _team_statistics(user=team.user, team=team)
    info["create_at"] = team.create_at
    location = dict()
    if team.location_id:
        location["location_id"] = team.location_id
        location["name"] = team.location.name
        location["ename"] = team.location.ename
        location["parent_id"] = team.location.parent.id
        location["parent_name"] = team.location.parent.name,
        location["parent_ename"] = team.location.parent.ename
    info["location"] = location
    return {"error_code": 0, "msg": "ok", "statistics": info}


"""
def weekstone_report(week_start, user=None, team=None, freelancer=False):
    #时薪报表，需求者传输team参数
    ws = list()
    # 计算星期一到星期日的日期
    week_end = week_start + datetime.timedelta(days=6)
    week_start = int(week_start.strftime("%Y%m%d"))
    week_end = int(week_end.strftime("%Y%m%d"))
    week_list = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    qs = (WeekStoneReport.period.between(week_start, week_end))
    if team:
        qs = qs & (WeekStoneReport.team == team)
    else:
        qs = qs & (WeekStoneReport.user == user) 
    weekreports = WeekStoneReport.select().where(qs)
    contracts = weekreports.group_by(WeekStoneReport.contract)

    all_amount, all_times = 0, 0
    for c in contracts:
        days = dict((day, "") for day in week_list) 
        wsr = weekreports.where(WeekStoneReport.contract == c).order_by(WeekStoneReport.period.desc())

        times = 0
        for w in wsr:
            times += w.times
            days[week_list[int(w.period - week_start)]] = "%s:%02d" % (int(times / 6), (times % 6 * 10))

        contract_name = c.contract.name
        hourly = c.contract.hourly
        times = "%s:%02d" % (int(times / 6), (times % 6 * 10)) 
        amount = c.contract.hourly / 6 * times 
        if freelancer:
            profile = c.contract.user.profile.first()
            f = {"id": c.user.uuid, "name": profile.name,
                 "avatar": widget.avatar(profile.avatar)}
        else:
            f = dict()
        all_amount += amount     
        all_times += times
        ws.append({"id": c.contract.uuid, "contract_name": contract_name, 
            "hourly": hourly, "times": times, "amount": amount, "days": days, 
            "freelancer": f})
    return ws, all_amount, all_times
"""
