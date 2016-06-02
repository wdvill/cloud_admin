#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from models.contract import (Contract, MileStone, WeekStone, ContractEvaluate, 
    ShotRecord,)
from models.job import Job
from models.margin import MarginRecord
from models.proposal import Proposal
from models.user import User
from models.team import Team
from models.notify import Notify, NotifyConfig, NotifySetting
from common import utils


#def notify_config_list(user, lang):
#    role = user.identify[0]
#    ncs = NotifyConfig.select().where(NotifyConfig.who == role)
#    out = []
#    for x in ncs:
#        out.append({"mtype":x.mtype, "name":x.name})
#    return {"error_code":0, "msg":"ok", "data":out}

def notify_setting_list(user):
    role, uid = user.identify[0], int(user.identify[1:])
    out = []
    if role == "f":
        ns = NotifySetting.select().where(NotifySetting.user==user)
        profile = user.profile.first()
        out.append({"mtype":"recomm_rate", "is_send":True, "rate":profile.recomm_rate})
    else:
        ns = NotifySetting.select().where(NotifySetting.team==uid)
    for x in ns:
        out.append({"mtype":x.mtype, "is_send":x.is_send})
    return {"error_code":0, "data":out}

# 通知设置
def notify_setting_update(user, params):
    role, uid = user.identify[0], int(user.identify[1:])
    mtype = params.get("mtype", "")
    is_send = params.get("is_send", "")
    rate = params.get("rate", "")
    if not mtype or is_send not in ("true", "false"):
        return {"error_code":20791, "msg":"params invalid"}
    if mtype == "recomm_rate":
        if rate not in ("day", "week"):
            return {"error_code":20792, "msg":"recommand rate error"}
        profile = user.profile.first()
        profile.recomm_rate = rate
        return {"error_code":0, "msg":"ok"}
    nt = NotifyConfig.select().where(NotifyConfig.mtype == mtype, NotifyConfig.who==role).first()
    if not nt:
        return {"error_code":20793, "msg":"notify not exist"}
    if role == "f":
        ns = NotifySetting.select().where(NotifySetting.user==uid, NotifySetting.mtype==mtype).first()
    else:
        ns = NotifySetting.select().where(NotifySetting.team==uid, NotifySetting.mtype==mtype).first()
    if not ns:
        ns = NotifySetting()
        if role == "f":
            ns.user = uid
        else:
            ns.team = uid
        ns.mtype = mtype
    ns.is_send = True if is_send == "true" else False
    ns.save()
    return {"error_code":0, "msg":"ok"}

# 用户消息查询
def notify_list(user, params):
    rtype = params.get("rtype")
    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    
    if not pagesize or not pagenum or not pagesize.isdigit() or not pagenum.isdigit():
        return {"error_code": 20661, "msg":"pagenation invalid"}
    
    pagenum, pagesize = int(pagenum), int(pagesize)
    if pagesize > 50:
        return {"error_code": 20661, "msg":"pagenation invalid"}

    if rtype not in ("number", "all", "read", "unread"):
        return {"error_code": 20662, "msg": "rtype invalid"}
    
    team = None
    if user.identify[0] != "f":
        team = Team.select().where(Team.id == user.identify[1:]).first()
        
    if team:
        notify = Notify.select().where(Notify.team == team)
    else:
        notify = Notify.select().where(Notify.user == user)

    if rtype == "number":
        notify = notify.where(Notify.read_at.is_null(True))
        return {"error_code": 0, "msg": "ok", "count": notify.count()}
    
    count_unread = 0
    if rtype == "read":
        notify = notify.where(Notify.read_at.is_null(False))
    elif rtype == "unread":
        notify = notify.where(Notify.read_at.is_null(True))
    else:
        count_unread = notify.where(Notify.read_at.is_null(True)).count()

    count = notify.count()
    notify = notify.order_by(Notify.create_at.desc()).paginate(pagenum, pagesize) 
    out = []
    for n in notify:
        tmp = {}
        tmp["id"] = n.id
        tmp["mtype"] = n.mtype
        tmp["title"] = n.title
        tmp["content"] = n.content
        tmp["extra"] = utils.loads(n.extra) if n.extra else ""
        tmp["read_at"] = utils.local_datetime_to_str(n.read_at)
        tmp["create_at"] = utils.local_datetime_to_str(n.create_at)
        out.append(tmp)
    return {"error_code": 0, "msg": "ok", "pagenum": pagenum, "count": count, 
            "notify": out, "count_unread": count_unread}


def notify_read(user, params):
    notify_id = params.get("notify_id")
    if not notify_id:
        return {"error_code": 20671, "msg": "notify_id invalid"}

    qs = (Notify.id == notify_id)
    if user.identify[0] != "f":
        qs = (qs & (Notify.team == int(user.identify[1:])))
    else:
        qs = (qs & (Notify.user == user))
    notify = Notify.select().where(qs).first()
    if not notify:
        return {"error_code": 20672, "msg": "notify not exists"}

    if notify.read_at:
        return {"error_code": 20673, "msg": "notify already read"}
    
    notify.read_at = utils.now()
    notify.save()
    return {"error_code": 0, "msg": "ok"}

def notify_delete(user, params):
    notify_id = params.get("notify_id")
    if not notify_id:
        return {"error_code": 20691, "msg": "notify_id invalid"}

    notify = Notify.select().where(Notify.id == notify_id, Notify.user == user)
    if user.identify[0] != "f":
        notify.where(Notify.team == user.identify[1:])
    notify = notify.first()
    if not notify:
        return {"error_code": 20692, "msg": "notify not exists"}
    notify.delete_instance()
    return {"error_code": 0, "msg": "ok"}

##############################################################################
# 消息类型
# 大类型_小类型, 如: contract_start, proposal_proposal
# 目前UI上没有显示消息类型，暂不做展示和映射


def _generate_notify(user, mtype, extra, title, content, team=None, etitle="", econtent=""):
    n = Notify()
    if team:
        n.team = team
    else:
        n.user = user
    n.mtype = mtype
    n.extra = extra
    n.title = title
    n.etitle = etitle
    n.content = content
    n.econtent = econtent
    n.save()


# 合同开始
def contract_start(body):
    if "contract_id" not in body:
        return
    contract_id = body['contract_id']

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_start"
    extra = utils.dumps({"uuid":contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "合同已经开始啦"
    content = "您的合同［{0}］已经生效".format(contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)

    profile = contract.user.profile.first()
    content = "您与［{0}］的合同［{1}］已经生效".format(profile.name, contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# 结束合同
def contract_freelancer_finish(body):
    if "contract_id" not in body:
        return
    contract_id = body['contract_id']

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_freelancer_finish"
    profile = contract.team.profile.first()
    extra = utils.dumps({"uuid":contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "你的合同已经结束啦"
    content = "你结束了与［{0}］的合同［{1}］".format(contract.team.name, contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)

    profile = contract.user.profile.first()
    content = "［{0}］结束了你们的合同［{1}］".format(profile.name, contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# 需求者结束合同
def contract_client_finish(body):
    if "contract_id" not in body:
        return
    contract_id = body['contract_id']

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_client_finish"
    profile = contract.team.profile.first()
    extra = utils.dumps({"uuid":contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "你的合同已经结束啦"
    content = "［{0}］结束了你们的合同［{1}］".format(contract.team.name, contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)

    profile = contract.user.profile.first()
    content = "你结束了与［{0}］的合同［{1}］".format(profile.name, contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# 暂停合同
def contract_client_pause(body):
    if "contract_id" not in body:
        return
    contract_id = body['contract_id']

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_client_pause"
    extra = utils.dumps({"uuid":contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "你的合同已经暂停"
    content = "［{0}］暂停了合同［{1}］，您将无法上传工作日志直至合同重新开启".format(
            contract.team.name, contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)
    content = "您暂停了合同［{0}］，服务方将无法上传工作日志直至合同重新开启".format(
            contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# 开启合同
def contract_client_restart(body):
    if "contract_id" not in body:
        return
    contract_id = body['contract_id']
    
    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_client_restart"
    extra = utils.dumps({"uuid":contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "你的合同重新开启"
    content = "［{0}］开启了合同［{1}］，您现在可以工作了。".format(
            contract.team.name, contract.name)
    profile = contract.user.profile.first()
    _generate_notify(contract.user, mtype, extra, title, content)

# 工作日志提交
def weekstone_freelancer_audit(body):
    """start:开始日期， end日志截止日期"""
    if "weekstone_id" not in body:
        return
    weekstone_id = body["weekstone_id"]

    weekstone = WeekStone.select().where(WeekStone.id == weekstone_id).first()
    contract = weekstone.contract
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    mtype = "weekstone_freelancer_audit"
    title = "您的工作日志已经提交啦"
    start = utils.datetime_to_date(weekstone.start_at)
    end = utils.datetime_to_date(weekstone.end_at)
    content = "您的合同［{0}］［{1}］-［{2}］的工作日志已提交给需求方。".format(
            contract.name, start, end)
    _generate_notify(contract.user, mtype, extra, title, content)
    profile = contract.user.profile.first()

    title = "{0}提交了工作日志请查看".format(profile.name)
    content = "你与［{0}］的合同［{1}］［{2}］-［{3}］的工作日志已提交给您，请在2天内检查并处理".format(
            profile.name, contract.name, start, end)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)


# 工作日志支付 
def weekstone_client_pass(body):
    if "weekstone_id" not in body:
        return

    weekstone = WeekStone.select().where(WeekStone.id == body["weekstone_id"]).first()
    start = utils.datetime_to_date(weekstone.start_at)
    end = utils.datetime_to_date(weekstone.end_at)
    contract = weekstone.contract
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    mtype = "weekstone_client_pass"
    title = "{0}已经付款".format(contract.team.name)
    content = "［{0}］支付了合同［{1}］［{2}］-［{3}］日工作日志报酬{4}元".format(
        contract.team.name, contract.name, start, end, utils.decimal_two(weekstone.actual_amount))
    _generate_notify(contract.user, mtype, extra, title, content)


# 开启下周时薪
def weekstone_next_week(body):
    if "weekstone_id" not in body:
        return
    weekstone = WeekStone.select().where(WeekStone.id == body["weekstone_id"]).first()
    start = utils.datetime_to_date(weekstone.start_at)
    end = utils.datetime_to_date(weekstone.end_at)
    contract = weekstone.contract
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    mtype = "weekstone_client_pass"
    title = "{0}开启了下周工作".format(contract.team.name)
    content = "［{0}］托管了合同［{1}］［{2}］-［{3}］日的费用，您现在可以工作了".format(
        contract.team.name, contract.name, start, end)
    _generate_notify(contract.user, mtype, extra, title, content)


# 添加里程碑
def milestone_create(body):
    if "milestone_id" not in body:
        return
    milestone_id = body["milestone_id"]
    
    milestone = MileStone.select().where(MileStone.id == milestone_id).first()
    mtype = "milestone_create"
    extra = utils.dumps({"contract_id": milestone.contract.uuid, "url": "/freelancers/contracts/%s" % milestone.contract.uuid})

    title = "你的合同增加一个里程碑"
    content = "［{0}］为您的合同［{1}］添加了一个新里程碑".format(
            milestone.contract.team.name, milestone.contract.name)
    _generate_notify(milestone.contract.user, mtype, extra, title, content)

# 服务方提请里程碑结款(通知需求方)
def milestone_freelancer_audit(body):
    if "milestone_id" not in body:
        return
    milestone_id = body["milestone_id"]
    
    milestone = MileStone.select().where(MileStone.id == milestone_id).first()
    mtype = "milestone_freelancer_audit"
    # 服务方提交审核后，需求发查看通知统一到合同详情页
    extra = utils.dumps({"contract_id":milestone.contract.uuid, "url": "/freelancers/contracts/%s" % milestone.contract.uuid})
    profile = milestone.contract.user.profile.first()

    title = "合同里程碑等待付款"
    content = "［{0}］请求支付合同［{1}］里程碑［{2}］，请及时查看处理".format(
        profile.name, milestone.contract.name, milestone.name)
    contract = milestone.contract
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# 需求方同意支付里程碑(通知服务方)
def milestone_client_pass(body):
    if "milestone_id" not in body:
        return
    milestone_id = body["milestone_id"]
    
    milestone = MileStone.select().where(MileStone.id == milestone_id).first()
    mtype = "milestone_client_pass"
    extra = utils.dumps({"contract_id": milestone.contract.uuid, "url": "/freelancers/contracts/%s" % milestone.contract.uuid})

    title = "合同里程碑已经付款"
    content = "［{0}］支付了合同［{1}］里程碑［{2}］［{3}］元".format(
            milestone.contract.team.name, milestone.contract.name, 
            milestone.name, milestone.actual_amount)
    _generate_notify(milestone.contract.user, mtype, extra, title, content)

# 需求方要求修改(通知服务方)
def milestone_client_unpass(body):
    if "milestone_id" not in body:
        return
    milestone_id = body["milestone_id"]
    
    milestone = MileStone.select().where(MileStone.id == milestone_id).first()
    mtype = "milestone_client_unpass"
    extra = utils.dumps({"contract_id": milestone.contract.uuid, "url": "/freelancers/contracts/%s" % milestone.contract.uuid})

    title = "合同里程碑需要进行修改再提交"
    content = "［{0}］拒绝了合同［{1}］里程碑［{2}］的结款申请，请沟通后重新提交".format(
            milestone.contract.team.name, milestone.contract.name, milestone.name)
    _generate_notify(milestone.contract.user, mtype, extra, title, content)

# 需求方拒绝投标(通知服务方)
def proposal_client_refuse(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_client_refuse"
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/freelancers/proposal/%s" % proposal.id})

    title = "你的投标被拒绝"
    content = "您对［{0}］的投标被雇主拒绝".format(proposal.job.name)
    _generate_notify(proposal.user, mtype, extra, title, content)

# 服务方拒绝邀请(通知需求方)
def proposal_freelancer_refuse(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_freelancer_refuse"

    profile = proposal.user.profile.first()
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/clients/jobs/%s#archive" % proposal.job.job_uuid})

    title = "你的邀请被拒绝"
    content = "［{0}］拒绝了您对［{1}］的投标邀请".format(profile.name, proposal.job.name)
    _generate_notify(proposal.team.user, mtype, extra, title, content, proposal.team)

# 开发者同意邀请(通知需求方)
def proposal_freelancer_accept(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_freelancer_accept"
    freelancer = proposal.user.profile.first()
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/clients/jobs/%s#interview" % proposal.job.job_uuid})

    title = "你的工作邀请被同意"
    content = "［{0}］同意了您的［{1}］工作邀请".format(freelancer.name, proposal.job.name)
    _generate_notify(proposal.team.user, mtype, extra, title, content, proposal.team)

# 需求方同意投标(通知服务方)
def proposal_client_accept(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_client_accept"

    title = "你的投标被同意"
    client = proposal.team.profile.first()
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/freelancers/proposal/%s" % proposal.id})
    content = "［{0}］同意了您的［{1}］投标".format(client.name, proposal.job.name)
    _generate_notify(proposal.user, mtype, extra, title, content)


# 需求方发出邀请
def proposal_client_active(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']
    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_client_active"
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/freelancers/proposal/%s" % proposal.id})

    title = "你收到了一个工作邀请"
    content = "您收到的工作邀请：［{0}］".format(proposal.job.name)
    _generate_notify(proposal.user, mtype, extra, title, content)


# 开发者新投标(项目有新投标)(通知需求方)
def proposal_freelancer_active(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_freelancer_active"
    freelancer = proposal.user.profile.first()
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/clients/jobs/%s#appli" % proposal.job.job_uuid})

    title = "你的项目有了新的投标"
    content = "［{0}］投标了您的项目［{1}］".format(freelancer.name, proposal.job.name)
    _generate_notify(proposal.team.user, mtype, extra, title, content, proposal.team)

# 开发者重新投标(通知需求方)
def proposal_freelancer_reactive(body):
    if "proposal_id" not in body:
        return
    proposal_id = body['proposal_id']

    proposal = Proposal.select().where(Proposal.id == proposal_id).first()
    mtype = "proposal_freelancer_reactive"
    freelancer = proposal.user.profile.first()
    extra = utils.dumps({"id": proposal.id, "job_id": proposal.job.job_uuid, "url": "/clients/jobs/%s#appli" % proposal.job.job_uuid})

    title = "你的项目被重新投标"
    content = "［{0}］重新投标了您的项目［{1}］".format(freelancer.name, proposal.job.name)
    _generate_notify(proposal.team.user, mtype, extra, title, content, proposal.team)


# 修改密码
def user_password_change(body):
    if "user_id" not in body:
        return
    user_id = body['user_id']

    user = User.select().where(User.id == user_id).first() 
    team = None
    if "team_id" in body and body["team_id"]:
        team = Team.select().where(Team.id == body['team_id']).first()
    # 我的名片页面 
    if team:
        url = "/clients/settings"
    else:
        url = "/freelancers/settings/concatinfo"
    extra = utils.dumps({"url": url})
    mtype = "user_password_change"

    title = "你修改了账号密码"
    content = "您修改了密码" 
    _generate_notify(user, mtype, extra, title, content, team)

# 密保问题创建
def user_question_create(body):
    if "user_id" not in body:
        return
    user_id = body['user_id']

    user = User.select().where(User.id == user_id).first() 
    team = None
    if "team_id" in body and body["team_id"]:
        team = Team.select().where(Team.id == body['team_id']).first()
    # 我的名片页面 
    if team:
        url = "/clients/settings"
    else:
        url = "/freelancers/settings/concatinfo"
    extra = utils.dumps({"url": url})
    mtype = "user_question_create"

    title = "密码保问题已创建"
    content = "您的密保问题已经创建" 
    _generate_notify(user, mtype, extra, title, content, team)

# 注册成功
def user_register(body):
    if "user_id" not in body:
        return
    user_id = body['user_id']

    user = User.select().where(User.id == user_id).first() 
    team = None
    if "team_id" in body and body["team_id"]:
        team = Team.select().where(Team.id == body['team_id']).first()

    if team:
        url = "/jobs/new"
    else:
        url = "/find-work-home"
    extra = utils.dumps({"url": url})
    mtype = "user_register"

    title = "恭喜注册成功"
    if team:
        content = "恭喜您已经注册成为云沃客需求方，发布您的第一个项目吧"
    else:
        content = "恭喜您已经注册成为云沃客服务方，开始发挥你的才能，找到第一份工作吧"
    _generate_notify(user, mtype, extra, title, content, team)

# 个人认证通过
def user_identify(body):
    if "user_id" not in body:
        return
    user_id = body['user_id']

    user = User.select().where(User.id == user_id).first() 
    team = None
    if "team_id" in body and body.get("team_id"):
        team = Team.select().where(Team.id == body['team_id']).first()

    if team:
        url = "/clients/settings/identify"
    else:
        url = "/freelancers/settings/identity"
    extra = utils.dumps({"url": url})
    mtype = "user_identify"

    title = "恭喜身份认证成功"
    content = "恭喜您，您已完成个人身份认证"
    _generate_notify(user, mtype, extra, title, content, team)

# 企业申请认证
def client_identify_apply(body):
    if "team_id" not in body:
        return
    team_id = body["team_id"]

    team = Team.select().where(Team.id == team_id).first()
    mtype = "client_identify_apply"

    title = "你提交了企业认证申请"
    content = "您已经提交了企业认证申请，请等待客服审核"
    extra = utils.dumps({"url": "/clients/settings/conidentify"})
    _generate_notify(team.user, mtype, extra, title, content, team)

# mark 企业认证通过
def client_identify_pass(team_id):
    team = Team.select().where(Team.id == team_id).first()
    mtype = "client_identify_pass"

    title = "企业认证通过"
    content = "恭喜您，您已完成企业认证"
    extra = utils.dumps({"url": "/clients/settings/conidentify"})
    _generate_notify(team.user, mtype, extra, title, content, team)

# mark 企业认证未通过
def client_identify_unpass(team_id):
    team = Team.select().where(Team.id == team_id).first()
    mtype = "client_identify_unpass"

    title = "企业认证不通过"
    content = "您的企业认证未通过，请重新认证"
    extra = utils.dumps({"url": "/clients/settings/conidentify"})
    _generate_notify(team.user, mtype, extra, title, content, team)

# 项目发布成功
def job_new(body):
    if "job_id" not in body:
        return
    job_id = body["job_id"]

    job = Job.select(Job.id, Job.job_uuid, Job.name, Job.user, Job.team).where(Job.id == job_id).first()
    mtype = "job_new"
    extra = utils.dumps({"job_id": job.job_uuid, "url": "/jobs/%s" % job.job_uuid})

    title = "你的项目发布成功"
    content = "您已成功发布项目［{0}］".format(job.name)
    _generate_notify(job.user, mtype, extra, title, content, job.team)

#  项目状态转换
def job_status_change(body):
    if "job_id" not in body:
        return
    job_id = body["job_id"]

    job = Job.select(Job.id, Job.user, Job.team, Job.job_uuid, Job.status, Job.name).where(Job.id == job_id).first()
    mtype = "job_status_change"
    extra = utils.dumps({"job_id": job.job_uuid, "url": "/jobs/%s" % job.job_uuid})
    job_status = dict(normal="公开", private="私有", close="关闭") 
    if job.status not in job_status:
        return

    title = "项目状态转换成功"
    content = "你的项目［{0}］已经成功转换为［{1}］状态".format(job.name, job_status.get(job.status))
    _generate_notify(job.user, mtype, extra, title, content, job.team)


# 发出offer 收到offer
def contract_new(body):
    if "contract_id" not in body:
        return
    contract_id = body["contract_id"]
    
    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_new"
    # 开发者和需求者offer详情页使用了同一个页面
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/offer/%s" % contract.uuid})
    title = "你收到了offer"
    content = "您收到了［{0}］发来的项目［{1}］offer".format(contract.team.name, contract.job.name)
    _generate_notify(contract.user, mtype, extra, title, content)
    
    profile = contract.user.profile.first()
    title = "你的offer已发出"
    content = "您已向［{0}］成功发送项目［{1}］offer".format(profile.name, contract.job.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)


# offer被拒绝 
def contract_refuse(body):
    if "contract_id" not in body:
        return
    contract_id = body["contract_id"]

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_refuse"
    profile = contract.user.profile.first()
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/offer/%s" % contract.uuid})

    title = "你的offer被拒绝"
    content = "［{0}］拒绝了您的的offer［{1}］".format(profile.name, contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# offer过期
def contract_expire(body):
    if "contract_id" not in body:
        return
    contract_id = body["contract_id"]

    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_expire"
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/offer/%s" % contract.uuid})
    title = "你的offer已过期"
    content = "你收到的offer［{0}］已过期".format(contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)

    content = "你发出的offer［{0}］已过期".format(contract.name)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)


# 撤消offer
def contract_revoke(body):
    if "contract_id" not in body:
        return
    contract_id = body["contract_id"]
    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_revoke"
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/offer/%s" % contract.uuid})
    title = "offer已被撤回"
    content = "［{0}］撤销了offer［{1}］".format(contract.team.name, contract.name)
    _generate_notify(contract.user, mtype, extra, title, content)


# 争议处理
def contract_dispute_start(body):
    if "contract_id" not in body:
        return
    contract = Contract.select().where(Contract.id == body["contract_id"]).first()
    # 计算争议金额
    amount = 0
    if contract.hourly == 0:
        stones = MileStone.select().where(MileStone.status == "dispute", MileStone.contract == contract)
        for s in stones:
            amount += s.amount
    else:
        ws = WeekStone.select().where(WeekStone.status == "dispute", WeekStone.contract == contract).first()
        if ws.shot_times > contract.workload * 6:
            pay_times = contract.workload * 6
            amount = contract.amount
        else:
            pay_times = ws.shot_times
            amount = utils.decimal_two(ws.shot_times * contract.hourly / 6)
    amount = utils.decimal_two(amount)

    mtype = "contract_dispute_start"
    extra = utils.dumps({"contract_id": contract.uuid, "url": "/freelancers/contracts/%s" % contract.uuid})
    title = "您的合同有争议款项"
    content = "您的合同［{0}］有一笔［{1}］的争议款，客服将在24小时内与您联系".format(contract.name, amount)
    _generate_notify(contract.user, mtype, extra, title, content)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)

# mark 争议处理完毕
def contract_dispute_finish(contract_id, amount, pay):
    """
    contract_id: 合同ID
    amount:争议金额
    pay:实际支付金额
    """
    contract = Contract.select().where(Contract.id == contract_id).first()
    mtype = "contract_dispute_finish"
    extra = utils.dumps({"contract_id": contract.uuid})

    title = "你的合同已处理完毕"
    content = "您的合同［{0}］有一笔［{amount}］的争议款，客服将在24小时内与您联系".format(contract.name, amount)
    _generate_notify(contract.user, mtype, extra, title, content)
    _generate_notify(contract.team.user, mtype, extra, title, content, contract.team)


# 充值成功
def margin_deposit_success(body):
    if "mrecord_id" not in body:
        return
    mrecord_id = body["mrecord_id"]

    record = MarginRecord.select().where(MarginRecord.id == mrecord_id).first()
    mtype = "margin_deposit_success"

    title = "充值成功"
    content = "你刚刚充值了［{0}］元，当前余额［{1}］元".format(record.amount, record.margin)
    team = record.team if record.team_id else None 
    extra = utils.dumps({"url": "/settings/account"})
    _generate_notify(record.user, mtype, extra, title, content, team)

# 提现成功
def margin_withdraw_success(body):
    if "mrecord_id" not in body:
        return
    mrcord_id = body["mrecord_id"]
    
    record = MarginRecord.select().where(MarginRecord.id == mrcord_id).first()
    mtype = "margin_withdraw_success"

    title = "提现成功"
    content = "你的提现申请［{0}］元已处理，［{1}］元已到账".format(record.amount, record.amount)
    team = record.team if record.team_id else None 
    extra = utils.dumps({"url": "/settings/account"})
    _generate_notify(record.user, mtype, extra, title, content, team)

# 申请提现
def margin_withdraw_apply(body):
    if "mrecord_id" not in body:
        return
    mrecord_id = body["mrecord_id"]

    record = MarginRecord.select().where(MarginRecord.id == mrecord_id).first()
    mtype = "margin_withdraw_apply"

    title = "你的提现申请已提交"
    content = "您申请提现［{0}］元，客服将在三个工作日内为您处理".format(record.amount)
    team = record.team if record.team_id else None 
    extra = utils.dumps({"url": "/settings/account"})
    _generate_notify(record.user, mtype, extra, title, content, team)

# 评价通知 
def contract_evaluate(body):
    if filter(lambda x: x not in body, ["contract_evaluate_id", "role"]):
        return
    eid = body["contract_evaluate_id"]
    ce = ContractEvaluate.select().where(ContractEvaluate.id == eid).first()
    if not ce:
        return

    mtype = "contract_evaluate"
    extra = utils.dumps({"uuid":ce.contract.uuid, "url": "/freelancers/contracts/%s" % ce.contract.uuid})
    title = "你收到一条新评价"
    if body["role"] == "f":
        # 通知需求方
        profile = ce.contract.user.profile.first()
        team = ce.contract.team
        content = "您与［{0}］的合同［{1}］对方已评价".format(profile.name, ce.contract.name)
        _generate_notify(team.user, mtype, extra, title, content, team)
    else:
        # 通知服务方
        profile = ce.contract.user.profile.first()
        content = "您与［{0}］的合同［{1}］对方已评价".format(ce.contract.team.name, ce.contract.name)
        _generate_notify(ce.contract.user, mtype, extra, title, content)


# 每周时薪第一次上传通知需求方
def weekstone_shot_first(body):
    if "weekstone_id" not in body:
        return
    ws = WeekStone.select().where(WeekStone.id == body["weekstone_id"]).first()
    mtype = "weekstone_shot_first"
    profile = ws.contract.user.profile.first()
    title = "时薪制项目{0}已经开始工作啦".format(profile.name)
    team = ws.contract.team
    extra = utils.dumps({"contract_id": ws.contract.uuid, "url": "/clients/freelancers/diary"})
    content = "［{0}］已经开始工作，请进入工作日志查看工作状况".format(profile.name)
    _generate_notify(team.user, mtype, extra, title, content, team)


# 开发者第一次上传工作日志
def freelancer_shot_first(body):
    if "shot_id" not in body:
        return
    shot = ShotRecord.select().where(ShotRecord.id == body["shot_id"]).first()
    mtype = "freelancer_shot_first"
    title = "您已经开始时薪制工作啦"
    extra = utils.dumps({"url": "/freelancers/diary"})
    content = "恭喜您已经开始工作了，请进入工作日志查看工作状况"
    _generate_notify(shot.user, mtype, extra, title, content)
    

