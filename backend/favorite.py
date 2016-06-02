#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from models.favorite import Favorite, Subscribe
from models.job import Job
from models.statistics import TeamStatistics
from models.user import User
from common import utils
from backend import widget


def favorite_list(user, params, lang):
    pagesize = utils.safe_id(params.get("pagesize", "10"))
    pagenum = utils.safe_id(params.get("pagenum", "1"))

    if pagesize is None or pagenum  is None:
        return {"error_code": 20281, "msg": "pagenation invalid"}

    if pagesize > 100:
        return {"error_code": 20282, "msg": "pagesize must less than 100"}

    utype, uid = user.identify[0], int(user.identify[1:])

    favorites = Favorite.select().where(Favorite.user == user)
    if utype == 'c':
        favorites = favorites.where(Favorite.ftype == 'REQ', Favorite.team == uid)
    else:
        favorites = favorites.where(Favorite.ftype == 'DEV', Favorite.team == 0)

    count = favorites.count()
    favorites = favorites.paginate(pagenum, pagesize)
    out = []
    stats_dic = {}
    for favorite in favorites:
        tmp = dict()
        tmp["favorite_id"] = favorite.id
        tmp["memo"] = favorite.memo
        tmp["create_at"] =  utils.local_datetime_to_str(favorite.create_at)
        if utype == 'c':
            obj = User.select().where(User.id == favorite.target_id).first()
            profile = obj.profile.first()
            tmp["favorite"] = {
                "uuid": obj.uuid, "name": profile.name,
                "avatar": widget.avatar(profile.avatar),
                "overview": profile.overview, "hourly": profile.hourly,
                "workload": profile.workload,
                "skills": utils.loads(profile.skills) if profile.skills else []
            }
            location = {}
            if profile.location_id:
                city = widget.get_location(profile.location_id)
                location["name"] = utils.lang_map_name(city.name, city.ename, lang)
                location["location_id"] = city.id

                if city.parent_id:
                    province = widget.get_location(city.parent_id)
                    location["parent_name"] = utils.lang_map_name(province.name, province.ename, lang)
                    location["parent_id"] = province.id
            tmp["favorite"]["location"] = location
        else:
            obj = Job.select().where(Job.id == favorite.target_id).first()
            tmp["job"] = {
                "id": obj.job_uuid, "name": obj.name,
                "description": obj.description, "level": obj.level,
                "duration": obj.duration, "workload": obj.workload,
                "paymethod": obj.paymethod, "budget": obj.budget,
                "skills": utils.loads(obj.skills) if obj.skills else [],
                "create_at": utils.local_datetime_to_str(obj.create_at),
                "hires": obj.hires,
                "category": utils.lang_map_name(obj.category.name, obj.category.ename, lang),
                "eveluate_num": 0,
                "aver_score": 0,
                "status": obj.status
            }
            # 统计数据查询
            if obj.team_id not in stats_dic:
                score = TeamStatistics.select(TeamStatistics.eveluate_num, TeamStatistics.aver_score).where(TeamStatistics.user == obj.user, TeamStatistics.team == obj.team).first()
                stats_dic[obj.team_id] = score
            else:
                if stats_dic[obj.team_id]:
                    tmp["job"]["eveluate_num"] = stats_dic[obj.team_id].eveluate_num
                    tmp["job"]["aver_score"] = stats_dic[obj.team_id].aver_score
        out.append(tmp)

    return {"error_code": 0, "msg": "ok", "count": count, "pagenum": pagenum, "favorites": out}


def favorite_create(user, params):
    target_id = params.get("target_id")
    memo = params.get("memo")
    if not target_id:
        return {"error_code": 20286, "msg": "target_id required"}

    if memo and len(memo) > 100:
        return {"error_code": 20287, "msg": "memo too long"}

    utype, uid = user.identify[0], int(user.identify[1:])
    if utype == 'c':
        obj = User.select().where(User.uuid == target_id).first()
    else:
        obj = Job.select().where(Job.job_uuid == target_id).first()
    if not obj:
        return {"error_code": 20283, "msg": "target_id invalid"}

    favorite = Favorite.select().where(Favorite.user == user, Favorite.target_id == obj.id)
    if utype == 'c':
        favorite = favorite.where(Favorite.ftype == 'REQ', Favorite.team == uid)
    else:
        favorite = favorite.where(Favorite.ftype == 'DEV', Favorite.team == 0)
    if favorite:
        return {"error_code": 20285, "msg": "already favorite"}

    favorite = Favorite()
    favorite.user = user
    favorite.target_id = obj.id
    if utype == 'c':
        favorite.ftype = 'REQ'
        favorite.team = uid
        if memo:
            favorite.memo = memo
    else:
        favorite.ftype = 'DEV'

    favorite.save()
    return {"error_code": 0, "msg": "ok"}

def favorite_delete(user, params):
    target_id = params.get("target_id")
    if not target_id:
        return {"error_code": 20288, "msg": "pagenation invalid"}

    utype, uid = str(user.identify[:1]), int(user.identify[1:])
    if utype == 'c':
        obj = User.select().where(User.uuid == target_id).first()
    else:
        obj = Job.select().where(Job.job_uuid == target_id).first()
    if not obj:
        return {"error_code": 20289, "msg": "target_id invalid"}

    favorites = Favorite.delete().where(Favorite.user == user, Favorite.target_id == obj.id)
    if utype == 'c':
        favorites = favorites.where(Favorite.ftype == 'REQ', Favorite.team == uid)
    else:
        favorites = favorites.where(Favorite.ftype == 'DEV', Favorite.team == 0)

    if not favorites:
        return {"error_code": 202810, "msg": "favorite not exists"}

    favorites.execute()
    return {"error_code": 0, "msg": "ok"}

def subscribe_list(user, params):
    utype, uid = str(user.identify[:1]), int(user.identify[1:])
    if utype != 'f':
        return {"error_code": 20291, "msg":"you are not freelancer"}

    subs = Subscribe.select().where(Subscribe.user == user)
    out = []
    for x in subs:
        out.append({"id":x.id, "name":x.name, "keyword": x.keyword})
        # out.append({"id":x.id, "name":x.name, "keyword": utils.loads(x.keyword)})

    return {"error_code": 0, "msg": "ok", "subscribes": out}

def subscribe_create(user, params):
    utype, uid = str(user.identify[:1]), int(user.identify[1:])
    if utype != 'f':
        return {"error_code": 20301, "msg":"you are not freelancer"}
    name = params.get("name", "")

    workload = params.get("workload")
    duration = params.get("duration")
    level = params.get("level")
    paymethod = params.get("paymethod")
    word = params.get("keyword","")

    if not name or len(name) > 20:
        return {"error_code": 20302, "msg":"parameters invalid"}

    keyword = {}
    if workload:
        try:
            keyword['workload'] = [int(x) for x in workload.split(",") if 0 < int(x) <= 3]
        except:
            return {"error_code": 20303, "msg":"workload invalid"}
    else:
        keyword['workload'] = ""

    if duration:
        try:
            keyword['duration'] = [int(y) for y in duration.split(",") if 0 < int(x) <= 5]
        except:
            return {"error_code": 20304, "msg":"duration invalid"}
    else:
        keyword['duration'] = ""

    if level:
        try:
            keyword['level'] = [x for x in level.split(",") if x in("entry", "middle", "expert")]
        except:
            return {"error_code": 20305, "msg":"level invalid"}
    else:
        keyword['level'] = ""
    if paymethod:
        try:
            keyword['paymethod'] = [y for y in paymethod.split(",") if y in ("hour", "fixed")]
        except:
            return {"error_code": 20306, "msg":"paymethod invalid"}
    else:
        keyword['paymethod'] = ""

    if word and len(word) > 30:
        return {"error_code": 20308, "msg":"keyword too long"}

    keyword['keyword'] = word

    c = Subscribe.select().where(Subscribe.user == user).count()
    if c >= 5:
        return {"error_code": 20307, "msg":"cannot large than five"}

    subscribe = Subscribe()
    subscribe.user = user
    subscribe.name = name
    subscribe.keyword = utils.dumps(keyword)
    subscribe.save()
    return {"error_code":0, "msg":"ok"}

def subscribe_delete(user, params):
    utype, uid = str(user.identify[:1]), int(user.identify[1:])
    if utype != 'f':
        return {"error_code": 20311, "msg":"you are not freelancer"}
    sub_id = params.get("subscribe_id", "")

    sub = Subscribe.select().where(Subscribe.id == sub_id).first()
    if sub and sub.user_id != user.id:
        return {"error_code": 20312, "msg":"this subscribe not exists"}
    if sub:
        sub.delete_instance()

    return {"error_code":0, "msg":"ok"}
