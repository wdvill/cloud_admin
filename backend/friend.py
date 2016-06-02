#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement
from models.friend import Friend
from models.user import User, Profile, UserRole
from models.team import Team, TeamProfile
from backend import widget

def friend_list(user, is_mobile):
    if is_mobile:
        role, uid = user.app_identify[0], int(user.app_identify[1:])
    else:
        role, uid = user.identify[0], int(user.identify[1:])
    out = []
    if role == "f":
        fs = Friend.select().where(Friend.user == uid, Friend.ftype=="f", Friend.status == "normal")
        for x in fs:
            team_profile = x.team.profile.first()
            avatar = widget.logo(x.team.logo)
            out.append({"id":x.team.id, "name":x.team.name, "avatar":avatar, "uuid":x.team.uuid})
    else:
        fs = Friend.select().where(Friend.team == uid, Friend.ftype == "c", Friend.status == "normal")
        for x in fs:
            profile = x.user.profile.first()
            out.append({"id":x.user.id, "name":profile.name, "avatar":widget.avatar(profile.avatar), 
                        "uuid":x.user.uuid, "title":profile.title})
    kefus = UserRole.select().where(UserRole.rtype == "kefu")
    service = []
    for k in kefus:
        profile = Profile.select(Profile.avatar, Profile.name).where(Profile.user == k.user).first()
        service.append({"id":k.user.id, "uuid":k.user.uuid, "name":profile.name, "avatar":widget.avatar(profile.avatar)})
    return {"error_code":0, "msg":"ok", "friends":out, "service":service}

# 此接口会出问题，应进行权限控制
def get_users_info(params):
    user_ids = params.get("user_ids")
    if user_ids:
        user_ids = [int(x) for x in user_ids.split(",") if x.isdigit()]
    if not user_ids:
        return {"erro_code":20511, "msg":"params invalid"}
    out = []
    if user_ids:
        users = Profile.select().join(User).where(Profile.user << user_ids)
        for x in users:
            out.append({"id":x.user_id, "name":x.name, "avatar":widget.avatar(x.avatar), "uuid":x.user.uuid})
            try:
                user_ids.remove(x.user_id)
            except:
                pass
    if user_ids:
        teams = Team.select().where(Team.id << user_ids)
        for y in teams:
            profile = y.profile.first()
            avatar = widget.logo(y.logo)
            out.append({"id":y.id, "name":y.name, "avatar":avatar, "uuid":y.uuid})

    return {"error_code":0, "msg":"ok", "users":out}
