#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import decimal

from models.attachment import Attachment
from models.contract import Contract
from models.favorite import Favorite
from models.proposal import Proposal, ProposalMessage
from models.job import Job
from models.user import User
from models.friend import IMGroup
from common import utils, queue
from config.settings import database
from backend import friend, widget


def proposal_create(user, params):
    """ 标操作
    需求者邀标
        标UUID、备注
    开发者投标
        标UUID、报价、备注、附件、预计完成时间
    """
    job_id = params.get("job_id")
    user_id = params.get("user_id")
    amount = params.get("amount")
    duration = utils.safe_id(params.get("duration", 0))
    message = params.get("message", "")
    attachment_id = utils.safe_id(params.get("attachment_id"))
    if not job_id:
        return {"error_code": 20341, "msg": "params invalid"}

    role = (str(user.identify[:1]), int(user.identify[1:]))

    job = Job.select().where(Job.job_uuid == job_id, Job.status == "normal").first()
    if not job:
        return {"error_code": 20342, "msg": "job not available"}

    if role[0] == "f" and job.user == user or role[0] != "f" and job.team.user != user:
        return {"error_code": 203419, "msg": "proposal user and job user invalid"}

    if attachment_id:
        attachment = Attachment.select().where(Attachment.id == attachment_id).first()
        if not attachment:
            return {"error_code": 203418, "msg": "attachment invalid"}

    # 开发者投标
    if role[0] == "f":
        ct = Contract.select().where(Contract.user == user, Contract.team == job.team, Contract.job == job, Contract.status << ("paid", "carry", "carry_pay", "dispute")).first()
        if ct:
            return {"error_code": 203421, "msg": "contract not finish, not allow proposal"}

        if not amount or not message: 
            return {"error_code": 20341, "msg": "params invalid"}

        if job.paymethod == "fixed" and (not duration or duration and duration not in xrange(1, 6)):
            return {"error_code": 203420, "msg": "duration invalid" }

        try:
            amount = decimal.Decimal(amount).quantize(decimal.Decimal("0.01"), context=decimal.Context(traps=[decimal.Inexact]))
        except:
            return {"error_code": 203415, "msg": "amount invalid"}

        proposal = Proposal.select().where(Proposal.user == user, Proposal.job == job, Proposal.status << ["active", "interview", "archive", "refuse"]).count()
        if proposal > 0:
            return {"error_code": 20343, "msg": "already proposal job"}

        proposal = Proposal()
        proposal.user = user
        proposal.job = job
        proposal.invite = job.user
        proposal.team = job.team
        proposal.ptype = 'D'
        proposal.status = 'active'
        proposal.price = amount
        if job.paymethod == "fixed":
            proposal.duration = duration
        proposal.message = message
        if attachment_id:
            proposal.attachment = attachment_id
        proposal.update_at = utils.now()
        proposal.save()

        queue.to_queue({"type":"proposal_freelancer_active", "proposal_id":proposal.id, "user_id":user.id})
        return {"error_code": 0, "msg": "ok"}

    # 需求者邀请投标
    else:
        if not user_id:
            return {"error_code": 20344, "msg": "freelancer required"}
        freelancer = User.select().where(User.uuid == user_id).first()
        if not freelancer:
            return {"error_code": 20344, "msg": "freelancer required"}
        
        ct = Contract.select().where(Contract.user == freelancer, Contract.team == job.team, Contract.job == job, Contract.status << ("paid", "carry", "carry_pay", "dispute")).first()
        if ct:
            return {"error_code": 203422, "msg": "contract not finish, not allow proposal"}

        proposal = Proposal.select().where(
            (Proposal.user == freelancer) & (Proposal.job == job) & (
                (Proposal.status == "refuse") | (
                    (Proposal.status != "refuse") & (Proposal.status != "active")
                ))).first()
        if proposal:
            return {"error_code": 203416, "msg": "not allow invite"}

        proposal = Proposal.select().where(Proposal.user == freelancer, Proposal.job == job, Proposal.status == "active").first()
        if not proposal:
            proposal = Proposal()
            proposal.user = freelancer
            proposal.job = job
            proposal.invite = user
            proposal.team = role[1]
            proposal.ptype = 'I'
            proposal.message = message
            proposal.status = 'active'

        proposal.update_at = utils.now()
        proposal.save()
        queue.to_queue({"type": "proposal_client_active", "proposal_id": proposal.id, "user_id":freelancer.id})
        return {"error_code": 0, "msg": "ok"}


def proposal_update(user, params):
    proposal_id = utils.safe_id(params.get('proposal_id'))
    operate = params.get("operate")

    if not proposal_id or not operate:
        return {"error_code": 20341, "msg": "params invalid"}

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    if not proposal:
        return {"error_code": 20346, "msg": "proposal not exists"}

    role = (str(user.identify[:1]), int(user.identify[1:]))
    if operate == "accept":
        return _proposal_accept(user, role, proposal, params)
    elif operate == "refuse":
        return _proposal_refuse(user, role, proposal, params)
    elif operate == "revoke":
        return _proposal_revoke(user, role, proposal, params)
    #elif operate == "hire":
    #    return _proposal_hire(user, role, proposal, params)
    elif operate == "archive":
        return _proposal_archive(user, role, proposal, params)
    elif operate == "reactive":
        return _proposal_reactive(user, role, proposal, params)
    elif operate == "unfreeze":
        return _proposal_unfreeze(user, role, proposal, params)
    else:
        return {"error_code": 20347, "msg": "Illegal operate"}


def _proposal_reactive(user, role, proposal, params):
    """ 重新投标
    开发者重新投标给出新报价
    """
    if not (role[0] == "f" and proposal.user == user
            and proposal.status in ("active", "interview")):
        return {"error_code": 20347, "msg": "Illegal operate"}
    amount = params.get("amount")
    message = params.get("message")
    if not amount:
        return {"error_code": 20341, "msg": "params invalid"}
    try:
        amount = decimal.Decimal(amount).quantize(decimal.Decimal("0.01"), context=decimal.Context(traps=[decimal.Inexact]))
    except:
        return {"error_code": 203415, "msg": "amount invalid"}

    proposal.price = amount
    if message:
        proposal.reason = message 
    proposal.update_at = utils.now()
    proposal.save()

    queue.to_queue({"type":"proposal_freelancer_reactive", "proposal_id":proposal.id})
    return {"error_code": 0, "msg": "ok"}


def _proposal_accept(user, role, proposal, params):
    """ 同意
    开发者同意被邀请，需求者同意投标
    """
    if not (role[0] == "f" and proposal.ptype == "I" and proposal.user == user
            or role[0] != "f" and proposal.ptype == "D" and proposal.team_id == role[1]):
        return {"error_code": 20347, "msg": "Illegal operate"}

    if proposal.status != "active":
        return _proposal_common_error(key=proposal.status)

    # 同意之后，投标状态变化为沟通中
    if role[0] == "f":
        # 开发者同意邀标时需要给出报价和备注
        amount = params.get("amount")
        message = params.get("message", "")
        if not amount:
            return {"error_code": 20341, "msg": "params invalid"}
        amount = utils.decimal_two(amount)
        if amount is None:
            return {"error_code": 203415, "msg": "amount invalid"}

        proposal.price = amount
        if message:
            proposal.reason = message

        now = utils.now()
        ca = proposal.create_at
        if now.year == ca.year and now.month == ca.month and now.day == ca.day:
            proposal.day_reply = True

    proposal.status = "interview"
    proposal.update_at = utils.now()
    proposal.save()

    #with database.atomic() as txn:
    #    try:
    #        friend.create_friend(proposal.user, proposal.team)
    #    except:
    #        return {"error_code": 203417, "msg": "create friendship fail"}

    # 通知im创建一个群组
    queue.to_queue({"type":"create_group", "group_name":proposal.job.name,
                "req_user_id":proposal.user_id, "user_id":proposal.user_id,
                "team_id":proposal.team_id, "proposal_id":proposal.id})

    if proposal.ptype == "I":
        queue.to_queue({"type":"proposal_freelancer_accept", "proposal_id":proposal.id, "user_id":proposal.user_id})
    else:
        queue.to_queue({"type":"proposal_client_accept", "proposal_id":proposal.id, "user_id":proposal.user_id})

    return {"error_code": 0, "msg": "ok"}


def _proposal_refuse(user, role, proposal, params):
    """ 拒绝
    开发者拒绝被邀请，需求者拒绝投标
    """
    if not (role[0] == "f" and proposal.ptype == "I" and proposal.user == user
            or role[0] != "f" and proposal.ptype == "D" and proposal.team_id == role[1]):
        return {"error_code": 20347, "msg": "Illegal operate"}

    if proposal.status not in ("active", "interview"):
        return _proposal_common_error(key=proposal.status)

    question_id = utils.safe_id(params.get("question_id"))
    message = params.get("message", "")
    if not question_id:
        return {"error_code": 203416, "msg": "refuse question invalid"}

    if proposal.ptype == "I":
        queue.to_queue({"type":"proposal_freelancer_refuse", "proposal_id":proposal.id})
    else:
        queue.to_queue({"type":"proposal_client_refuse", "proposal_id":proposal.id})

    proposal.question = question_id
    if message:
        proposal.reason = message
    proposal.status = "refuse"
    proposal.update_at = utils.now()
    proposal.save()
    return {"error_code": 0, "msg": "ok"}



def _proposal_revoke(user, role, proposal, params):
    """ 撤销
    开发者撤销投标，需求者不允许撤销邀请
    """
    if not (role[0] == "f" and proposal.user == user and proposal.status in ("active", "interview", "archive")):
        return {"error_code": 20347, "msg": "Illegal operate"}

    question_id = utils.safe_id(params.get("question_id"))
    message = params.get("message", "")
    if not question_id:
        return {"error_code": 203416, "msg": "refuse question invalid"}

    proposal.question = question_id
    if message:
        proposal.reason = message
    proposal.status = "revoke"
    proposal.update_at = utils.now()
    proposal.save()
    return {"error_code": 0, "msg": "ok"}


def client_send_offer(contract):
    """ 需求者给开发者发送offer """
    proposal = Proposal.select().where(Proposal.user == contract.user, Proposal.team == contract.team, Proposal.job == contract.job, Proposal.status != "hire").first()
    if not proposal:
        proposal = Proposal()
        proposal.user = contract.user 
        proposal.job = contract.job
        proposal.team = contract.team
        proposal.invite = contract.team.user
        proposal.ptype = "I"
        
    proposal.status = "hire"
    proposal.contract = contract
    proposal.update_at = utils.now()
    proposal.save()

    # 通知im创建一个群组
    queue.to_queue({"type":"create_group", "group_name":proposal.job.name,
                "req_user_id":proposal.user_id, "user_id":proposal.user_id,
                "team_id":proposal.team_id, "proposal_id":proposal.id,
                "contract_id": contract.id})

    return proposal


#def _proposal_hire(user, role, proposal, params):
#    """ 雇佣
#    需求者雇佣开发者操作，雇佣后可以发送offer
#    """
#    if not (role[0] != "f" and proposal.team_id == role[1]):
#        return {"error_code": 20347, "msg": "Illegal operate"}
#
#    # 沟通中、归档中 允许雇佣
#    if proposal.status not in ("interview", "archive"):
#        return _proposal_common_error(key=proposal.status)
#
#    proposal.status = "hire"
#    proposal.update_at = utils.now()
#    proposal.save()
#    return {"error_code": 0, "msg": "ok"}


def _proposal_archive(user, role, proposal, params):
    """ 归档
    开发者归档：沟通中开发者可以归档集冻结
    需求者归档：需求者处于归档状态，只是将标放到归档文件夹中
    """

    if not (role[0] == "f" and proposal.status == "interview" and proposal.user == user
            or role[0] != "f" and proposal.archive_c == False and proposal.team_id == role[1]):
        return {"error_code": 20347, "msg": "Illegal operate"}

    if role[0] == "f":
        proposal.status = "archive"
    else:
        question_id = utils.safe_id(params.get("question_id"))
        message = params.get("message", "")
        if not question_id:
            return {"error_code": 203416, "msg": "refuse question invalid"}
        proposal.question = question_id
        if message:
            proposal.reason = message
        proposal.archive_c = True
    proposal.update_at = utils.now()
    proposal.save()
    return {"error_code": 0, "msg": "ok"}



def _proposal_unfreeze(user, role, proposal, params):
    """ 解冻
    开发者归档解冻后变成沟通中，需求者归档解冻后变成正常
    """
    if not (role[0] == "f" and proposal.status == "archive" and proposal.user == user
            or role[0] != "f" and proposal.archive_c == True and proposal.team_id == role[1]):
        return {"error_code": 20347, "msg": "Illegal operate"}

    if role[0] == "f":
        proposal.status = "interview"
    else:
        proposal.archive_c = False
    proposal.update_at = utils.now()
    proposal.save()
    return {"error_code": 0, "msg": "ok"}


def _proposal_common_error(key):
    error = {
        "active": [20348, "Proposal active status"],
        "refuse": [20349, "Proposal already refuse"],
        "revoke": [203410, "Proposal already revoke"],
        "interview": [203411, "Proposal already interview"],
        "hire": [203412, "Proposal already hire"],
        "archive": [203413, "Proposal already archive"],
    }

    value = error[key]
    if not value:
        value = [203414, "Illegal proposal status"]
    return dict(zip(["error_code", "msg"], value))


def _job_apply_number(job_id):
    """根据工作ID统计数据
    applied: 申请人数
    interview: 正在沟通中
    """
    applied = Proposal.select().where(Proposal.job == job_id, Proposal.price != "").count()
    #applied = Proposal.select().where(Proposal.job == job_id, Proposal.ptype=='D', Proposal.is_view==False).count()
    interview = Proposal.select().where(Proposal.job == job_id, Proposal.status == "interview").count()
    return {"applied": applied, "interview": interview}

def proposal_list_basic(user, params, lang):
    operate = params.get("operate", "interview")
    #if operate not in ("interview", "invite", "active"):
    #    return {"error_code": 30002, "msg": "operate invalid"}

    role, uid = user.identify[0], int(user.identify[1:])
    # 开发者
    if role == "f":
        # 沟通中
        qs = Proposal.select().where(Proposal.user==uid, Proposal.status==operate)
        contracts = Contract.select().where(Contract.user==uid, Contract.status << ("carry", "service", "dispute", "finish", "paid"))
    else:
        qs = Proposal.select().join(Job).where(Proposal.team==uid, Proposal.status==operate)
        contracts = Contract.select(Contract.id,Contract.name).where(Contract.team==uid, Contract.status << ("carry", "service", "dispute", "finish", "paid"))
    out = {"interview":[], "all":[]}
    for x in qs:
        img = IMGroup.select().where(IMGroup.proposal == x).first()
        if not img:
            continue
        out["interview"].append({"id":x.id, "name":x.job.name, "group_id":img.im_group_id, "update_at":utils.local_datetime_to_str(x.update_at)})

    for y in contracts:
        img = IMGroup.select().where(IMGroup.contract == y).first()
        if not img:
            continue
        out["all"].append({"name":y.name, "group_id":img.im_group_id, "update_at":utils.local_datetime_to_str(y.accept_at)})

    return {"error_code":0, "msg":"ok", "proposals":out}

def proposal_list(user, params, lang):
    proposal_id = utils.safe_id(params.get("proposal_id"))
    job_id = params.get("job_id")
    operate = params.get("operate")

    role = (user.identify[0], int(user.identify[1:]))

    if proposal_id and operate:
        return {"error_code": 203423, "msg": "proposal_id and operate not allow together"}

    if operate and role[0] == "f" and operate not in ("interview", "invite", "active", "freeze"):
        return {"error_code": 30002, "msg": "operate invalid"}

    elif operate and role[0] == "c" and operate not in ("active", "hire", "archive", "interview", "invite"):
        return {"error_code": 30001, "msg": "operate invalid"}

    count = 0
    qs = None
    if proposal_id:
        qs = (Proposal.id == proposal_id)
    if job_id:
        job = Job.select().where(Job.job_uuid == job_id).first()
        if not job:
            return {"error_code": 20342, "msg": "job not exists"}
        #qs = (qs & (Proposal.job == job) if qs else (Proposal.job == job))
        qs = (Proposal.job == job)
    # 开发者
    if role[0] == "f":
        qs = (qs & (Proposal.user == user) if qs else (Proposal.user == user))
        # 沟通中
        if operate == "interview":
            qs = (qs & (Proposal.status == "interview"))
        # 投标未处理
        if operate == "active":
            qs = (qs & (Proposal.status == "active") & (Proposal.ptype == "D"))
        # 收到邀请
        if operate == "invite":
            qs = (qs & (Proposal.status == "active") & (Proposal.ptype == "I"))
        # 冻结中
        if operate == "freeze":
            qs = (qs & (Proposal.status << ["refuse", "revoke", "archive", "hire"]))
    # 需求者
    else:
        #qs = (qs & (Proposal.invite == user) if qs else (Proposal.invite == user))
        qs = (qs & (Proposal.team == role[1]) if qs else (Proposal.team == role[1]))
        # 申请中
        if operate == "active":
            qs = (qs & ((Proposal.archive_c == False) & (Proposal.status == "active") & (Proposal.ptype == "D")))
        # 沟通中
        if operate == "interview":
            # 邀请的投标展示在沟通中列表，但是不计数
            qs_interview = (qs & (Proposal.status << ("interview", "archive")) & (Proposal.archive_c == False)) 
            count = Proposal.select().where(qs_interview).count()
            qs = (qs & (Proposal.archive_c == False) & ((Proposal.status << ("interview", "archive")) | ((Proposal.status == "active") & (Proposal.ptype == "I"))) ) 
        # 已雇佣
        if operate == "hire":
            qs = (qs & (Proposal.archive_c == False) & (Proposal.status == "hire") & (Contract.status.in_(["paid", "carry", "pause", "finish", "dispute", "service"])))
            proposals = Proposal.select(Proposal).join(Contract, on=(Proposal.contract == Contract.id)).where(qs)
            count = proposals.count()
        # 已归档
        if operate == "archive":
            # 已归档：archive：ture
            # 撤销的offer：proposal-status:hire, contract-status:revoke 
            # 我拒绝的申请人：proposal-status:refuse, proposal-ptype:D
            # 拒绝邀请的申请人：proposal-status:refuse, proposal-ptype:I
            # 拒绝offer的申请人：proposal-status:hire, contract-status:refuse
            # offer失效的申请人：proposal-status:hire, contract-status:expire
            qs1 = (qs & ((Proposal.archive_c == True) | (Proposal.status == "refuse")))
            qs2 =  (qs & ((Proposal.status == "hire") & (Proposal.contract == Contract.id) & (Contract.status.in_(["revoke", "refuse", "expire"]))))
            t1 = Proposal.select(Proposal).where(qs1)
            t2 = Proposal.select(Proposal).join(Contract, on=(Proposal.contract == Contract.id)).where(qs2)
            count = t1.count() + t2.count()
            proposals = (t1 | t2)
        # app端查询邀请
        if operate == "invite":
            qs = (qs & (Proposal.archive_c == False) & (Proposal.status == "active") & (Proposal.ptype == "I"))
    
    if operate != "archive" and operate != "hire":
        proposals = Proposal.select(Proposal).where(qs)
        proposals = proposals.order_by(Proposal.create_at.desc())
        if not count:
            count = proposals.count()

    out = []
    for proposal in proposals:
        tmp = dict()
        tmp["proposal_id"] = proposal.id
        tmp["invite"] = {"name": proposal.team.name, "team_id": proposal.team.uuid}
        tmp["ptype"] = proposal.ptype
        tmp["status"] = proposal.status
        tmp["archive"] = proposal.archive_c
        tmp["price"] = proposal.price
        tmp["message"] = proposal.message
        tmp["reason"] = proposal.reason
        tmp["create_at"] = utils.local_datetime_to_str(proposal.create_at)
        tmp["update_at"] = utils.local_datetime_to_str(proposal.update_at)
        attachment = {}
        if proposal.attachment_id:
            attachment["id"] = proposal.attachment.id
            attachment["name"] = proposal.attachment.name
            attachment["size"] = proposal.attachment.size
            attachment["path"] = widget.attach(proposal.attachment.path)
        tmp["attachment"] = attachment
        tmp["duration"] = proposal.duration
        tmp["contract_id"] = proposal.contract.uuid if proposal.contract_id else ""
        tmp["contract_status"] = proposal.contract.status if proposal.contract_id else ""
        tmp["contract_name"] = proposal.contract.name if proposal.contract_id else ""
        b = proposal.job
        cate = widget.get_category(b.category_id)
        cate_parent = widget.get_category(cate.parent_id)

        tmp["job"] = {
            "id": b.job_uuid, "name": b.name, "paymethod": b.paymethod, 
            "description": b.summary, "budget": b.budget, "level": b.level, 
            "category": cate.name,
            #"category": {
            #    "id": cate.id, "name": cate.name,
            #    "parent_id": cate_parent.id, "parent_name": cate_parent.name},
            "workload": b.workload, "duration": b.duration, "create_at": utils.local_datetime_to_str(b.create_at)}
        tmp["job"].update(_job_apply_number(proposal.job.id))
        if proposal.question_id:
            tmp["question"] = _proposal_refuse_question(proposal.question, lang)
        
        tmp["user"] = dict()
        tmp["user"]["freelancer"] = _proposal_user_info(proposal.user, lang=lang)
        if role[0] != "c":
            favorite = Favorite.select().where(Favorite.user == proposal.team.user, Favorite.team == proposal.team, Favorite.target_id == proposal.user.id, Favorite.ftype == 'REQ').first()
            tmp["user"]["freelancer"]["is_favorite"] = True if favorite else False
        elif role[0] == "f":
            tmp["user"]["client"] = _proposal_user_info(proposal.invite, proposal.team)

        out.append(tmp)
    return {"error_code": 0, "msg": "ok", "proposals": out, "count": count}


def _proposal_refuse_question(question, lang):
    if lang=="zh_CN":
        return question.name
    return question.ename

def _proposal_user_info(user, team=None, lang="zh_CN"):
    info = dict()
    profile = user.profile.first()
    # freelancer
    if team is None:
        info["id"] = user.uuid
        info["name"] = profile.name
        info["title"] = profile.title
        info["avatar"] = widget.avatar(profile.avatar)
        info["hourly"] = profile.hourly
        location = {}
        if profile.location_id:
            city = widget.get_location(profile.location_id)
            location["name"] = utils.lang_map_name(city.name, city.ename, lang)
            if city.parent_id:
                province = widget.get_location(city.parent_id)
                location["parent_name"] = utils.lang_map_name(province.name, province.ename, lang)
            else:
                location["parent_name"] = ""
        info["location"] = location
        info["skills"] = utils.loads(profile.skills) if profile.skills else []
    # client
    else:
        info["id"] = user.uuid
        info["name"] = team.name
        info["avatar"] = widget.avatar(profile.avatar)
    return info


def send_message(user, params):
    proposal_id = utils.safe_id(params.get('proposal_id'))
    contract_id = params.get("contract_id", "")
    content = params.get("content", "")

    if not proposal_id and not contract_id or not content:
        return {"error_code": 20641, "msg": "params invalid"}

    if len(content) > 1024 * 4:
        return {"error_code": 20642, "msg": "message too long"}

    if proposal_id:
        proposal = Proposal.select().where(Proposal.id == proposal_id).first()
        if not proposal:
            return {"error_code": 20643, "msg": "proposal not exists"}
    else:
        contract = Contract.select().where(Contract.uuid==contract_id).first()
        if not contract:
            return {"error_code": 20643, "msg": "proposal not exists"}
        proposal = Proposal.select().where(Proposal.contract==contract).first()
        if not proposal:
            return {"error_code":20643, "msg":"proposal not exist"}

    role, uid = user.identify[0], int(user.identify[1:])
    if uid == proposal.user_id or uid == proposal.team_id:
        pass
    else:
        return {"error_code": 20644, "msg": "no authority"}

    topic = "%s-%s-%s" % (proposal.user_id, proposal.id, proposal.team_id)
    pm = ProposalMessage()

    if role == "f":
        pm.user = proposal.user
    else:
        pm.team = proposal.team
    pm.topic = topic
    pm.content = content
    pm.save()
    # 冻结之后发消息不回自动解冻, 招投标未处理的时候无法发送消息
    #if proposal.status in ("active", "archive"):
    if proposal.status == "active":
        proposal.status = "interview"
        proposal.save()
    
    # 检查是否已创建群
    g = IMGroup.select().where(IMGroup.proposal==proposal).first()
    if not g:
        queue.to_queue({"type":"create_group", "group_name":proposal.job.name,
                    "req_user_id":proposal.user_id, "user_id":proposal.user_id,
                    "team_id":proposal.team_id, "proposal_id":proposal.id})

    return {"error_code":0, "msg":"ok"}

def proposal_message_list(user, params):
    proposal_id = utils.safe_id(params.get('proposal_id'))
    pagesize = params.get("pagesize", "20")
    pagenum = params.get("pagenum", "1")

    if not proposal_id:
        return {"error_code": 20651, "msg": "params invalid"}

    if not pagesize or not pagenum or not pagesize.isdigit() or not pagenum.isdigit():
        return {"error_code": 20654, "msg":"pagenation invalid"}

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    if not proposal:
        return {"error_code": 20652, "msg": "proposal not exists"}

    role, uid = user.identify[0], int(user.identify[1:])
    if uid == proposal.user_id or uid == proposal.team_id:
        pass
    else:
        return {"error_code": 20653, "msg": "no authority"}

    pagesize = int(pagesize)
    pagenum = int(pagenum)

    topic = "%s-%s-%s" % (proposal.user_id, proposal.id, proposal.team_id)
    qs = ProposalMessage.select().where(ProposalMessage.topic==topic).order_by(ProposalMessage.create_at.desc())
    count = qs.count()
    msgs = qs.paginate(pagenum, pagesize)
    out = []
    profile = proposal.user.profile.first()
    username = profile.name
    teamname = proposal.team.name
    for x in msgs:
        if x.user_id:
            out.append({"name":username, "content":x.content, "create_at":utils.local_datetime_to_str(x.create_at)})
        else:
            out.append({"name":teamname, "content":x.content, "create_at":utils.local_datetime_to_str(x.create_at)})
    return {"error_code":0, "msg":"ok", "messages":out, "pagenum":pagenum, "count":count}
