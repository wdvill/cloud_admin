#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import logging
import datetime
import decimal
import traceback

from common import utils, validate, queue
from config.settings import database
from models.address import Address
from models.attachment import Attachment
from models.user import User, Profile, UserCategory
from models.category import Category
from models.favorite import Favorite
from models.statistics import UserStatistics
from models.team import Team, TeamProfile
from models.friend import Friend
from models.contract import (ShotRecord, Contract, MileStone, 
        MarginContractRecord, WeekStone, OrderBonus, MileStoneRecord)
from models.job import Job
from models.margin import Order, MarginRecord
from backend import widget, misc
from backend import statistics
from peewee import fn

logger = logging.getLogger(__name__)

def has_publish_check(user):
    job = Job.select(Job.id).where(Job.team==user.identify[1:]).first()
    if job:
        return True
    return False

def search_freelancer(user, params, lang):
    categorys = params.get("categorys", "")
    hourly_range = utils.safe_id(params.get("hourly_range", ""))
    rate = params.get("coop_rate", "")
    keyword = params.get("keyword", "")

    pagenum = utils.safe_id(params.get("pagenum", "1"))
    pagesize = utils.safe_id(params.get("pagesize", "10"))

    if not pagenum or not pagesize:
        return {"error_code": 20681, "msg":"pagenum or pagesize invalid"}

    if categorys:
        try:
            categorys = categorys.split(",")
            for category_id in categorys:
                if not category_id.isdigit():
                    raise
        except:
            return {"error_code": 20682, "msg": "categorys invalid"}

    qs = None
    if hourly_range == 0: # 不限
        pass
    elif hourly_range == 1: # 50元以下
        qs = Profile.hourly < 50
    elif hourly_range == 2: # 50-100元
        qs = Profile.hourly.between(50, 100)
    elif hourly_range == 3: # 100-150元
        qs = Profile.hourly.between(100, 150)
    elif hourly_range >= 4:
        qs = Profile.hourly > 150
    else:
        pass

    if keyword:
        qs_keyword = (Profile.name.contains(keyword) | Profile.skills.contains(keyword))
        qs = qs & qs_keyword if qs else qs_keyword 

    profile = Profile.select().where(qs)
    if categorys:
        _users = UserCategory.select(UserCategory.user).where(UserCategory.category << categorys).group_by(UserCategory.user)
        profile = profile.where(Profile.user << _users)
    profile = profile.join(User, on=(Profile.user == User.id)).where(User.status == "active", User.to_dev == True)
    count = profile.count()
    profile = profile.paginate(pagenum, pagesize)

    if not user:
        team_id = None
    else:
        team_id = int(user.identify[1:])

    out = []
    user_ids = []
    for x in profile:
        obj = {"id":x.user.uuid, "name":x.name, "skills":utils.loads(x.skills) if x.skills else [],
                    "title":x.title, "overview":x.overview, "avatar":widget.avatar(x.avatar),
                    "hourly":x.hourly, "favorite":False, "coop_rate":x.coop_rate, 'hours':0}
        user_ids.append(x.user.id)

        if team_id:
            related =  Favorite.select().where(Favorite.ftype == "REQ", Favorite.team==team_id, Favorite.target_id==x.user.id).first()
            if related:
                obj['favorite'] = True
        stats = UserStatistics.select().where(UserStatistics.user==x.user).first()
        if stats:
            obj['hours'] = stats.hours
        
        location = ''
        if x.location_id:
            if lang=="zh_CN":
                location = "%s,%s" % (x.location.parent.name, x.location.name)
            else:
                location = "%s,%s" % (x.location.parent.ename, x.location.ename)
        obj['location'] = location
        out.append(obj)

    queue.to_queue({"type":"user_discover", "user_ids":user_ids})

    return {"error_code":0, "msg":"ok", "count":count, "users":out, "pagenum":pagenum}


def client_profile(user, params, lang):
    #team_id = params.get("team_id", "")
    #if team_id:
    #    team = Team.select().where(Team.uuid == team_id).first()
    #    if not team:
    #        return {"error_code": 20551, "msg": "team not exists"}
    #else:
    #    team = user.team.first()
    team = Team.select().where(Team.id == int(user.identify[1:])).first()
    
    user = team.user
    profile = team.profile.first()
    freelancer = user.profile.first()

    out = dict()
    out["id"] = team.uuid
    out["freelancer"] = {"id": user.uuid, "name": freelancer.name, 
        "avatar": widget.avatar(freelancer.avatar) if freelancer.avatar else "", 
        "is_verify": True if freelancer.id_number else False,
        "id_number": freelancer.id_number,
        "phone": user.phone,
    }
    out["alipay"] = freelancer.alipay
    out["team_name"] = team.name
    out["status"] = team.status
    out["imid"] = team.id
    location = dict()
    if team.location_id:
        location["id"] = team.location_id
        location["name"] = utils.lang_map_name(team.location.name, team.location.ename, lang)
        location["parent_id"] = team.location.parent_id
        location["parent_name"] = utils.lang_map_name(team.location.parent.name, team.location.parent.ename, lang)
    out["location"] = location 
    out["link"] = team.link

    # add company verify status: uncheck, checking, pass, unpass
    is_verify, reason = "uncheck", ""
    if team.is_verify:
        is_verify = "pass"
    else:
        key, value = misc.generate_verify_init_data(user, "company_verify")
        m = misc.misc_get_or_create(key=key, value=value)
        misc_value = utils.loads(m.value)
        verify_status = misc_value.get("status")
        if verify_status:
            is_verify = verify_status
            reason = misc_value.get("reason")
    out["company_verify"] = {"is_verify": is_verify, "reason": reason}

    # profile
    out["logo"] = widget.logo(team.logo) 
    out["overview"] = profile.overview
    out["address"] = profile.address
    out["phone"] = profile.phone
    out["email"] = profile.email
    out["company_name"] = profile.company_name
    out["contact"] = profile.contact
    out["contact_phone"] = profile.contact_phone
    out["permit_number"] = "%s***%s" % (profile.permit_number[:4], profile.permit_number[-4:]) if profile.permit_number else ""
    out["org_number"] = "%s***%s" % (profile.org_number[:3], profile.org_number[-3:]) if profile.org_number else ""
    out["permit_img"] = widget.picture(profile.permit_img.path) if profile.permit_img_id else ""
    out["org_img"] = widget.picture(profile.org_img.path) if profile.org_img_id else ""
    return {"error_code": 0, "msg": "ok", "profile": out}


def client_profile_update(user, params):
    name = params.get("name")
    team_name = params.get("client_name")
    link = params.get("link")
    overview = params.get("overview")
    location_id = utils.safe_id(params.get("location_id"))
    address = params.get("address")
    phone = params.get("phone")
    email = params.get("email")
    
    team = Team.select().where(Team.id == user.identify[1:]).first()
    if not team or user.identify[0] == "f":
        return {"error_code": 20541, "msg": "user role invalid"}

    profile = team.profile.first()

    if name is not None:
        if len(name) == 0 or len(name) > 30:
            return {"error_code": 20548, "msg": "name invalid"}
        freelancer = user.profile.first()
        if freelancer.id_number:
            return {"error_code": 20549, "msg": "name verify, not allow modify"}
        freelancer.name = name
        freelancer.save()
            
    if team_name is not None:
        if len(team_name) == 0 or len(team_name) > 150:
            return {"error_code": 20542, "msg": "team name invalid"}
        if team.is_verify is True:
            return {"error_code": 205410, "msg": "company is verify, not allow modify name"}
        team.name = team_name

    if link is not None:
        if len(link) > 100:
            return {"error_code": 20543, "msg": "link invalid"}
        team.link = link

    if location_id:
        location = Address.select().where(Address.id == location_id).first()
        if not location:
            return {"error_code": 20544, "msg": "location_id invalid"}
        team.location = location 

    if address is not None:
        if len(address) == 0 or len(address) > 100:
            return {"error_code": 20545, "msg": "address invalid"}
        profile.address = address

    if phone is not None:
        phone = str(phone).strip()
        if phone and (len(phone) == 0 or len(phone) > 20):
            return {"error_code": 20546, "msg": "phone invalid"}
        profile.phone = phone

    if email is not None:
        if email and not validate.is_email(email):
            return {"error_code": 20547, "msg": "email invalid"}
        profile.email = email

    if overview is not None:
        if len(overview) == 0:
            return {"error_code": 205411, "msg": "overview invalid"}
        profile.overview = overview
    
    team.save()
    profile.save()
    return {"error_code": 0, "msg": "ok"}


def client_verify(user, params):
    company_name = params.get("company_name")
    name = params.get("name")
    phone = params.get("phone")
    permit_number = params.get("permit_number")
    org_number = params.get("org_number")
    permit_id = utils.safe_id(params.get("permit_id"))
    org_id = utils.safe_id(params.get("org_id"))

    team = Team.select().where(Team.id == user.identify[1:]).first()
    if team.is_verify:
        return {"error_code": 20566, "msg": "already verify"}
    profile = team.profile.first()

    if not company_name or not name or not phone or not permit_number or not org_number or (not permit_id and not profile.permit_img_id) or (not org_id and not profile.org_img_id):
        return {"error_code": 20561, "msg": "params invalid"}

    if len(company_name) > 150:
        return {"error_code": 20567, "msg": "company_name too long"}
    
    if len(name) > 20:
        return {"error_code": 20562, "msg": "name too long"}
    
    if len(phone) > 20:
        return {"error_code": 20563, "msg": "phone too long"}
    
    if permit_id:
        permit = Attachment.select().where(Attachment.user == user, Attachment.id == permit_id).first()
        if not permit:
            return {"error_code": 20564, "msg": "permit_id invalid"}
    
    if org_id:
        org = Attachment.select().where(Attachment.user == user, Attachment.id == org_id).first()
        if not org:
            return {"error_code": 20565, "msg": "permit_id invalid"}
    
    # add company verify misc, for admin verify unpass reason
    key, value = misc.generate_verify_init_data(user, "company_verify")
    m = misc.misc_get_or_create(key=key, value=value)
    misc_value = utils.loads(m.value)
    # company verify, do not check verify times
    # if misc_value['id_verify_count'] >= 3:
    #     return {"error_code": 20263, "msg": "verify too many times"}
    misc_value["id_verify_count"] += 1
    misc_value["last_verify_time"] = utils.now()
    misc_value["status"] = "checking"
    misc_value["reason"] = ""
    misc.misc_update(key, misc_value)
    
    profile.company_name = company_name 
    profile.contact = name
    profile.contact_phone = phone
    profile.permit_number = permit_number
    profile.org_number = org_number
    if permit_id:
        profile.permit_img = permit
    if org_id:
        profile.org_img = org
    profile.save()

    # send msg to user
    queue.to_queue({"type": "client_identify_apply", "team_id": team.id})
    return {"error_code": 0, "msg": "ok"}

def get_client_freelancers(user):
    team_id = int(user.identify[1:])
    fs = Friend.select(Friend.user).where(Friend.team==team_id).group_by(Friend.user)
    out = []
    for x in fs:
        profile = x.user.profile.first()
        out.append({"id":x.user.uuid, "name":profile.name})
    return {"error_code":0, "msg":"ok", "users":out}


def week_summary_report(user, params):
    """ 需求者按时付费周报 """
    start_at = utils.str_to_date(params.get("start_at"), utc=False)
    end_at = utils.str_to_date(params.get("end_at"), utc=False)
    if not start_at or not end_at:
        return {"error_code": 20591, "msg": "params invalid"}
    
    start_at = utils.str_to_date(params.get("start_at"), utc=True)
    end_at = utils.str_to_date(params.get("end_at"), utc=True)
    qs = ((Contract.team == int(user.identify[1:])) & (Order.status == "success") & (Order.confirm_at.between(start_at, end_at))) 
    qs_ms = (qs & (MileStone.status << ["finish", "service"]))
    qs_ws = (qs & (WeekStone.status << ["finish", "service"]))
    qs_bonus = ((OrderBonus.status == "success") & (OrderBonus.confirm_at.between(start_at, end_at)) & (OrderBonus.team == int(user.identify[1:])))

    ms_list, ws_list, amount_bonus = list(), list(), 0
    ms = MileStone.select().join(Contract, on=(MileStone.contract == Contract.id)).join(Order, on=(MileStone.pay_order == Order.id)).where(qs_ms).order_by(Order.confirm_at.asc())
    for m in ms:
        profile = m.contract.user.profile.first()
        record = m.record.order_by(MileStoneRecord.create_at.desc()).first()
        ms_list.append({
            "contract_name": m.contract.name,
            "contract_id": m.contract.uuid,
            "stone_name": m.name,
            "start_at": utils.local_datetime_to_str(m.start_at),
            "end_at": utils.local_datetime_to_str(record.audit_at),
            "actual_amount": m.actual_amount,
            "freelancer": {
                "id": profile.user.uuid, 
                "name": profile.name, 
                "avatar": widget.avatar(profile.avatar)
            }
        })

    ws = WeekStone.select().join(Contract, on=(WeekStone.contract == Contract.id)).join(Order, on=(WeekStone.pay_order == Order.id)).where(qs_ws).order_by(Order.confirm_at.asc())
    for m in ws:
        profile = m.contract.user.profile.first()
        ws_list.append({
            "contract_name": m.contract.name,
            "contract_id": m.contract.uuid,
            "start_at": utils.local_datetime_to_str(m.start_at),
            "end_at": utils.local_datetime_to_str(m.end_at),
            "shot_times": m.shot_times * 10,
            "actual_amount": m.actual_amount,
            "freelancer": {
                "id": profile.user.uuid, 
                "name": profile.name, 
                "avatar": widget.avatar(profile.avatar)
            }
        })
    # 结算奖金，日期内发放的奖金
    bonus = OrderBonus.select(fn.sum(OrderBonus.amount) + fn.sum(OrderBonus.fee)).where(qs_bonus).scalar()
    return {"error_code": 0, "msg": "ok", "weekstones": ws_list, "milestones": ms_list, "bonus": bonus}


def budget_report(user, params):
    """ 需求者预算报表 """
    start_at = utils.str_to_date(params.get("start_at"), utc=False)
    end_at = utils.str_to_date(params.get("end_at"), utc=False)
    if not start_at or not end_at:
        return {"error_code": 20591, "msg": "params invalid"}
    
    start_at = utils.datetime_day_min(start_at, utc=True)
    end_at = utils.datetime_day_max(end_at, utc=True)
    c_list = list()
    qs = ((Contract.team == int(user.identify[1:])) & (Contract.hourly == 0) & 
            (Contract.status << ["carry", "finish", "pause", "dispute", "service"]) & 
            (Contract.accept_at.between(start_at, end_at)))

    contracts = Contract.select().where(qs).order_by(Contract.accept_at.asc())
    for c in contracts:
        profile = c.user.profile.first()
        c_list.append({
            "contract_name": c.name,
            "contract_id": c.uuid,
            "amount": c.amount,
            "actual_amount": c.total_amount,
            "freelancer": {
                "id": profile.user.uuid, 
                "name": profile.name, 
                "avatar": widget.avatar(profile.avatar)
            }
        }) 
    return {"error_code": 0, "msg": "ok", "contracts": c_list}


def timesheet_report(user, params):
    """ 需求者工时查询 """
    freelancer_id = params.get("freelancer_id")
    start_at = utils.str_to_date(params.get("start_at"), utc=False)
    end_at = utils.str_to_date(params.get("end_at"), utc=False)
    if not start_at or not end_at:
        return {"error_code": 20841, "msg": "params invalid"}

    start_at = utils.datetime_day_min(start_at, utc=True)
    end_at = utils.datetime_day_max(end_at, utc=True)
    ws_list = list()
    freelancer = None
    if freelancer_id:
        freelancer = User.select().where(User.uuid == freelancer_id).first()
        if not freelancer:
            return {"error_code": 20842, "msg": "freelancer not exists"}
    
    qs = ((Contract.team == int(user.identify[1:])) & (Contract.hourly > 0) & 
            (Contract.status << ["carry", "finish", "pause", "dispute", "service"]))
    if freelancer:
        qs = (qs & (Contract.user == freelancer))

    ws = WeekStone.select(WeekStone).where(
        WeekStone.status << ["finish", "service"] 
    ).join(Contract, on=(WeekStone.contract == Contract.id)).where(
        qs
    ).join(Order, on=(WeekStone.pay_order == Order.id)).where(
        Order.status == "success", 
        Order.confirm_at.between(start_at, end_at)
    ).order_by(Order.confirm_at.asc())

    for w in ws:
        # 计算时薪周金额
        if w.shot_times > w.contract.workload * 6:
            shot_times = w.contract.workload * 6
            actual_amount = w.contract.amount
        else:
            shot_times = w.shot_times
            actual_amount = utils.decimal_two(w.shot_times * w.contract.hourly / 6)

        audit_record = w.record.first()
        profile = w.contract.user.profile.first()
        ws_list.append({
            "contract_name": w.contract.name,
            "contract_id": w.contract.uuid,
            "shot_times": shot_times * 10,
            "actual_amount": utils.decimal_two(actual_amount),
            "freelancer": {
                "id": profile.user.uuid, 
                "name": profile.name, 
                "avatar": widget.avatar(profile.avatar)
            },
            "audit_at": utils.local_datetime_to_str(audit_record.create_at) if audit_record else "",
        })
    return {"error_code": 0, "msg": "ok", "weekstones": ws_list}
    

def contract_margin_record(user, params):
    user_id = params.get("user_id")
    start_at = utils.str_to_datetime(params.get('start_at'), pattern='%Y-%m-%d', utc=False)
    if not start_at or start_at.weekday() != 0:
        return {"error_code": 20601, "msg": "start_at must be monday"}
    end_at = start_at + datetime.timedelta(days=6)
    
    records = MarginContractRecord.select(MarginContractRecord).join(MarginRecord).where(MarginRecord.record_type.in_(["pay", "refund", "freeze"])).switch(MarginContractRecord)
    if user_id:
        freelancer = User.select().where(User.uuid == user_id).first()
        if not freelancer:
            return {"error_code": 20602, "msg": "user_id invalid"}
            
        records = recsords.join(MarginRecord).where(MarginRecord.user == freelancer).switch(MarginContractRecord)
    records = records.join(Order).where(Order.status == "success", Order.confirm_at.between(start_at, end_at)).order_by(Order.confirm_at.desc()).switch(MarginContractRecord)
    out = []
    freeze, pay, refund = 0, 0, 0
    for r in records:
        tmp = dict()
        tmp["pay_at"] = utils.local_datetime_to_str(r.order.confirm_at)
        tmp["ptyoe"] = r.margin_record.record_type
        profile = r.margin_record.user.profile.first()
        tmp["freelancer_name"] = profile.name
        tmp["contract_name"] = r.contract.name
        tmp["amount"] = r.margin_record.amount
        if r.contract.job.paymenthod == "fixed":
            tmp["milestone_name"] = r.milestone.name
        if r.margin_record.record_type == "freeze":
            freeze += r.margin_record.amount
        elif r.margin_record.record_type == "pay":
            pay += r.margin_record.amount
        elif r.margin_record.record_type == "refund":
            refund += r.margin_record.amount
        out.append(tmp)
    return {"error_code": 0, "msg": "ok", "records": out, "freeze": freeze, "pay": pay, "refund": refund}
  
