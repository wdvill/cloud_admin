#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement
import ujson as json
import requests
import logging
from config.settings import imserver
from models.friend import Friend, IMGroup
from models.proposal import Proposal
from models.contract import Contract

logger = logging.getLogger(__name__)

# 创建好友关系
def create_friend(user, team):
    result = {"error_code":0, "msg":"ok"}
    if not team:
        return {"error_code":20501, "msg":"team not exist"}
    f_1 = Friend.select().where(Friend.user == user, Friend.team == team, Friend.ftype=="f").first()
    if f_1:
        if f_1.status != "normal":
            f_1.status = "normal"
            f_1.save()
    else:
        f_1 = Friend()
        f_1.user = user
        f_1.team = team
        f_1.ftype = "f"
        f_1.save()

    f_2 = Friend.select().where(Friend.user == user, Friend.team == team, Friend.ftype=="c").first()
    if f_2:
        if f_2.status != "normal":
            f_2.status = "normal"
            f_2.save()
    else:
        f_2 = Friend()
        f_2.user = user
        f_2.team = team
        f_2.ftype = "c"
        f_2.save()
    return result

def create_group(body):
    if "user_id" not in body or "team_id" not in body:
        return

    if "contract_id" not in body and "proposal_id" not in body:
        return

    # 有contract_id 表示要发offer

    create_friend(body["user_id"], body["team_id"])

    if "proposal_id" not in body:
        return

    prop = Proposal.select().where(Proposal.id == body["proposal_id"]).first()
    if not prop:
        return

    img = IMGroup.select().where(IMGroup.proposal == prop).first()
    if not img:
        uri = "%s/create_group" % imserver
        param = {"req_user_id":body["req_user_id"], "group_name":body["group_name"],
                "group_type":3, "token":"abc", "group_avatar":"", "user_id_list":[body["user_id"], body["team_id"]]}
        headers = {'user-agent': 'yunzujia async create group by zhenjing'}
        # {"error_code":0,"error_msg":"成功","group_id":194}
        try:
            res = requests.post(uri, headers=headers, data=json.dumps(param))
            logger.error("im server: %s, %s" % (res.status_code, res.content))

            cont = json.loads(res.content)
            if cont['error_code'] == 0:
                img = IMGroup()
                img.proposal = body["proposal_id"]
                if "contract_id" in body:
                    img.contract = body["contract_id"]
                img.im_group_id = cont['group_id']
                img.save()

                if "contract_id" in body:
                    contract = prop.contract
                    send_offer(contract, body, cont["group_id"])
            return
        except:
            logger.error("im server cannot connected")
            return

    if "contract_id" in body:
        contract = Contract.select().where(Contract.id == body["contract_id"]).first()
        group_id = img.im_group_id
        img.contract = contract
        img.save()

        send_offer(contract, body, group_id)


def send_offer(contract, body, group_id):
    msg_uri = "%s/send_msg" % imserver
    param = {"req_id": body["team_id"], "to_id": group_id, 
            "msg_content": {"title":"收到了一个offer", "name": contract.name, 
                        "id": contract.uuid, "type":"offer", "status": contract.status,
                        "paymethod": "fixed"}, 
            "token": "132323", "msg_type": 9}
    if contract.hourly > 0:
        param["msg_content"]["paymethod"] = "hour"

    headers = {'user-agent': 'yunzujia async create group by zhenjing'}
    try:
        res = requests.post(msg_uri, headers=headers, data=json.dumps(param))
        logger.error("im server: %s, %s" % (res.status_code, res.content))

        #cont = json.loads(res.content)
    except:
        logger.error("im server connot connected")
