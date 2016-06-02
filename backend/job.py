#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import decimal

from common import utils, queue
from models.category import Category
from models.attachment import Attachment
from models.job import Job
from models.team import Team
from models.favorite import Favorite
from models.statistics import TeamStatistics
from models.proposal import Proposal
from models.contract import Contract
from models.user import User, UserCategory
from backend import widget


def new_job(user, params):
    name = unicode(params.get("name"))
    category_id = utils.safe_id(params.get("category_id"))
    skills = params.get("skills")
    duration = utils.safe_id(params.get("duration"))
    workload = utils.safe_id(params.get("workload"))
    level = params.get("level")
    hires = utils.safe_id(params.get("hires"))
    attachment_id = params.get("attachment_id")
    description = params.get("description")
    stage = params.get("stage")
    budget = params.get("budget", "0")
    paymethod = params.get("paymethod")
    platforms = params.get("platforms")
    api = params.get("api", "")
    languages = params.get("languages")
    frameworks = params.get("frameworks")

    status = params.get("status", "normal")

    if not name or not description or not hires or not category_id or not paymethod or not level:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(name) > 100 or len(description) > 3000:
        return {"error_code": 20011, "msg": "name or description too long"}

    summary = unicode(utils.replace_html_tag(description))[:100]

    # hires 数字 招聘人数
    if category_id == False or category_id <= 0 or hires == False or hires < 1:
        return {"error_code": 20012, "msg": "category or hires invalid"}

    if paymethod not in ("hour", "fixed"):
        return {"error_code": 20013, "msg": "paymethod invalid"}

    # duration ( 1-5 ) 代表时间长短
    # workload ( 1-3 ) 代表时间长短
    if paymethod == "hour" and (not 1 <= workload <= 3 or not 1 <= duration <= 5):
        return {"error_code": 200117, "msg": "duration or workload invalid"}

    if stage:
        if stage not in ("design", "introduction", "none", "idea"):
            return {"error_code": 20014, "msg": "stage invalid"}
    else:
        stage = "none"

    if level not in ("entry", "middle", "expert"):
        return {"error_code": 20016, "msg": "level invalid"}

    if api:
        try:
            api = api.split(",")
            if not isinstance(api, list):
                raise
            for x in api:
                if x not in ("social", "pay", "storage", "other"):
                    raise
        except:
            return {"error_code": 20017, "msg": "params api invalid"}

    if platforms:
        try:
            platforms = platforms.split(",")
            if not isinstance(platforms, list):
                raise
            for x in platforms:
                if x not in ("android", "iphone", "ipad", "winphone", "windows", "mac", "other", "linux"):
                    raise
        except:
            return {"error_code": 20018, "msg": "direct platform invalid"}
    else:
        platforms = ""

    if frameworks:
        try:
            frameworks = frameworks.split(",")
            if not isinstance(frameworks, list) or len("".join(frameworks)) >= 200:
                raise
        except:
            return {"error_code": 20116, "message": "frameworks invalid"}
    else:
        frameworks = ""

    if languages:
        try:
            languages = languages.split(",")
            if not isinstance(languages, list):
                raise
        except:
            return {"error_code": 20019, "msg": "require language invalid"}
    else:
        languages = ""

    if skills:
        try:
            skills = skills.split(",")
            if not isinstance(skills, list):
                raise
            if len(skills) > 5:
                raise
        except:
            return {"error_code": 200110, "msg": "skills invalid little than 5"}

    cate, attach, amount = None, None, None

    if paymethod == "hour":
        amount = 0
    else:
        amount = utils.decimal_two(budget)
        if not amount:
            return {"error_code": 200111, "msg": "budget invalid"}

    try:
        cate = Category.get(Category.id == category_id)
    except:
        return {"error_code": 200112, "msg": "category invalid"}

    if attachment_id and utils.safe_id(attachment_id):
        try:
            attach = Attachment.get(Attachment.id == attachment_id)
        except:
            return {"error_code": 200113, "msg": "attachment not exists"}
    else:
        attach = 0

    tmp_job = Job.select().where(Job.user==user, Job.name==name).first()
    if tmp_job:
        return {"error_code": 200114, "msg": "job is exists"}

    team_id = int(user.identify[1:])
    job = Job()
    job.team = team_id
    job.user = user
    job.name = name
    job.category = cate
    job.attachment = attach
    job.skills = utils.dumps(skills) if skills else ""
    if paymethod == "hour":
        job.duration = duration
        job.workload = workload

    job.level = level
    job.hires = hires
    job.description = description
    job.summary = summary
    job.stage = stage
    job.budget = amount
    job.paymethod = paymethod

    if status == "draft":
        job.status = "draft"
    else:
        job.status = "normal"

    job.platforms = utils.dumps(platforms) if platforms else ""
    job.languages = utils.dumps(languages) if languages else ""
    job.integrated_api = utils.dumps(api) if api else ""
    job.frameworks = utils.dumps(frameworks) if frameworks else ""

    job.save()
    if status == "normal":
        queue.to_queue({"type": "job_new", "job_id": job.id, "team_id": team_id})
    return {"error_code": 0, "msg": "ok", "job_id": job.job_uuid}


# 更新工作
def edit_job(user, params):
    job_id = params.get("job_id")

    name = unicode(params.get("name"))
    category_id = utils.safe_id(params.get("category_id", "0"))
    skills = params.get("skills")
    duration = utils.safe_id(params.get("duration", "0"))
    workload = utils.safe_id(params.get("workload", "0"))
    level = params.get("level")
    hires = utils.safe_id(params.get("hires", "0"))
    attachment_id = utils.safe_id(params.get("attachment_id", "0"))
    description = params.get("description")
    stage = params.get("stage")
    budget = params.get("budget", 0)
    paymethod = params.get("paymethod")
    platforms = params.get("platforms")
    api = params.get("api", "")
    languages = params.get("languages")
    frameworks = params.get("frameworks")


    job = Job.select().where(Job.job_uuid == job_id).first()
    if not job or job.user_id != user.id:
        return {"error_code":1, "msg":"job not exists"}

    if name and len(name) < 100:
        job.name = name

    if description:
        if len(description) > 3000:
            return {"error_code":1, "msg":"job description too long"}

        job.summary = unicode(utils.replace_html_tag(description))[:100]
        job.description = description

    # hires 数字 招聘人数
    if category_id != False and category_id > 0 and category_id != job.category_id:
        job.category = category_id
    if hires != False and hires >0 and hires != job.hires:
        job.hires = hires

    # duration ( 1-5 ) 代表时间长短
    # workload ( 1-3 ) 代表时间长短
    if job.paymethod == "hour":
        if workload > 0 and 1 <= workload <= 3:
            job.workload = workload

        if duration > 0 and 1 <= duration <= 5:
            job.duration = duration

    if stage:
        if stage in ("design", "introduction", "none", "idea") and stage != job.stage:
            job.stage = stage

    if level and level in ("entry", "middle", "expert") and level != job.level:
        job.level = level

    if api:
        try:
            api = api.split(",")
            if not isinstance(api, list):
                raise
            for x in api:
                if x not in ("social", "pay", "storage", "other"):
                    raise
            job.integrated_api = utils.dumps(api)
        except:
            return {"error_code": 20017, "msg": "params api invalid"}

    if platforms:
        try:
            platforms = platforms.split(",")
            if not isinstance(platforms, list):
                raise
            for x in platforms:
                if x not in ("android", "iphone", "ipad", "winphone", "windows", "mac", "other", "linux"):
                    raise
            job.platforms = utils.dumps(platforms)
        except:
            return {"error_code": 20018, "msg": "direct platform invalid"}

    if frameworks:
        try:
            frameworks = frameworks.split(",")
            if not isinstance(frameworks, list):
                raise
            job.frameworks = utils.dumps(frameworks)
        except:
            return {"error_code": 20116, "message": "frameworks invalid"}

    if languages:
        try:
            languages = languages.split(",")
            if not isinstance(languages, list):
                raise
            job.languages = utils.dumps(languages)
        except:
            return {"error_code": 20019, "msg": "require language invalid"}

    if skills:
        try:
            skills = skills.split(",")
            if not isinstance(skills, list):
                raise
            job.skills = utils.dumps(skills)
        except:
            return {"error_code": 200110, "msg": "skills invalid"}

    cate, attach, amount = None, None, None
    if amount:
        amount = utils.decimal_two(amount)
        if not amount:
            return {"error_code": 200111, "msg": "budget invalid"}
        job.budget = amount

    if category_id:
        try:
            cate = Category.get(Category.id == category_id)
        except:
            return {"error_code": 200112, "msg": "category invalid"}
        job.category = category_id

    if attachment_id:
        try:
            attach = Attachment.get(Attachment.id == attachment_id)
        except:
            return {"error_code": 200113, "msg": "attachment not exists"}
        job.attachment = attachment_id

    job.save()
    return {"error_code": 0, "msg": "ok", "job_id": job.job_uuid}

def search(user, params):
    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    if not pagesize or not pagenum or not pagesize.isdigit() or not pagenum.isdigit():
        return {"error_code": 20071, "msg":"pagenation invalid"}

    budget_range = params.get("budget_range", "")

    workload = params.get("workload")
    duration = params.get("duration")
    level = params.get("level")
    paymethod = params.get("paymethod")
    categorys = params.get("categorys", "")
    keyword = params.get("keyword", "")
    
    if workload:
        try:
            workload = [int(x) for x in workload.split(",") if 0 < int(x) <= 3]
        except:
            return {"error_code": 20072, "msg":"workload invalid"}
    else:
        workload = None

    if duration:
        try:
            duration = [int(y) for y in duration.split(",") if 0 < int(x) <= 5]
        except:
            return {"error_code": 20073, "msg":"duration invalid"}
    else:
        duration = None

    if level:
        try:
            level = [x for x in level.split(",") if x in ("entry", "intermediate", "expert")]
        except:
            return {"error_code": 20074, "msg":"level invalid"}
    else:
        level = None
    if paymethod:
        try:
            paymethod = [y for y in paymethod.split(",") if y in ("hour", "fixed")]
        except:
            return {"error_code": 20075, "msg":"paymethod invalid"}
    else:
        paymethod = None

    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20076, "msg":"pagesize must less than 100"}

    if categorys:
        try:
            categorys = categorys.split(",")
            for category_id in categorys:
                if not category_id.isdigit():
                    raise
        except:
            return {"error_code": 20077, "msg":"category invalid"}

    if keyword and len(keyword) > 200:
        return {"error_code": 20079, "msg":"keyword length is 1-200"}

    budget_start, budget_end = 0, 0 
    if budget_range:
        budget_start, budget_end = budget_range.split(",")
        try:
            budget_start, budget_end = int(budget_start), int(budget_end)
        except:
            return {"error_code": 200710, "msg":"budget range invalid"}

    records, count = [], 0
    qs = None
    if workload:
        qs = Job.workload << workload
    if duration:
        qs = qs & Job.duration << duration if qs else Job.duration << duration
    if level:
        qs = qs & Job.level << level if qs else Job.level << level
    if paymethod:
        qs = qs & Job.paymethod << paymethod if qs else Job.paymethod << paymethod
    if categorys:
        qs = qs & Job.category << categorys if qs else Job.category << categorys
    if keyword:
        qs = qs & Job.name.contains(keyword) if qs else Job.name.contains(keyword)

    if budget_start and budget_end:
        qs = qs & Job.budget.between(budget_start, budget_end) if qs else Job.budget.between(budget_start, budget_end)

    if qs:
        qs = qs & (Job.status == "normal")
    else:
        qs = (Job.status == "normal")
        
    count = Job.select().where(qs).count()
    records = Job.select().where(qs).order_by(Job.create_at.desc()).paginate(pagenum, pagesize)

    jobs = []
    stats_dic = {}
    for obj in records:
        tmp = {"name": obj.name, 
               "description": obj.summary,
               "duration": obj.duration,
               "skills": utils.loads(obj.skills) if obj.skills else [],
               "workload": obj.workload, "paymethod": obj.paymethod,
               "budget": obj.budget,
               "level": obj.level,
               "create_at": utils.local_datetime_to_str(obj.create_at),
               "category": widget.get_category(obj.category_id).name,
               "hires": obj.hires,
               "id": obj.job_uuid,
               "eveluate_num": 0,
               "aver_score": 0,
               }
        # 是否收藏
        tmp["favorite"] = False
        if user and user.identify[0] == "f":
            favorites = Favorite.select(Favorite.id).where(Favorite.user == user, Favorite.target_id == obj.id)
            favorites = favorites.where(Favorite.ftype == 'DEV', Favorite.team == 0).first()
            if favorites:
                tmp["favorite"] = True
        # 评价统计
        if obj.team_id not in stats_dic:
            score = TeamStatistics.select(TeamStatistics.eveluate_num, 
                                TeamStatistics.aver_score).where(TeamStatistics.user == obj.user, 
                                TeamStatistics.team == obj.team).first()
            stats_dic[obj.team_id] = score
        else:
            if stats_dic[obj.team_id]:
                tmp["eveluate_num"] = stats_dic[obj.team_id].eveluate_num
                tmp["aver_score"] = stats_dic[obj.team_id].aver_score
        jobs.append(tmp)
    return {"error_code": 0, "msg": "ok", "count": count, "jobs": jobs, "pagenum": pagenum}

_hourly_range = {"entry": "<100", "middle": "100-300", "expert": '300'}

def get_job(uuid, user=None, lang="zh_CN"):
    obj = Job.select().where(Job.job_uuid == uuid, Job.status!="delete").first()
    if not obj:
        return {"error_code": 20081, "msg":"job not exists"}

    # 非项目发布者只允许查看开放的项目
    # if not user or user and obj.team_id != int(user.identify[1:]):
    #    if obj.status != "normal":
    #        return {"error_code": 20081, "msg":"job not exists"}

    cate = widget.get_category(obj.category_id)
    cate_parent = widget.get_category(cate.parent_id)

    res_job = {"name": obj.name, "description":obj.description,
               "duration":obj.duration,
               "skills":utils.loads(obj.skills) if obj.skills else [],
               "workload":obj.workload, "paymethod":obj.paymethod,
               "stage":obj.stage, "budget":obj.budget,
               "level":obj.level, "hires":obj.hires,
               "platforms": utils.loads(obj.platforms) if obj.platforms else [],
               "frameworks": utils.loads(obj.frameworks) if obj.frameworks else [],
               "languages": utils.loads(obj.languages) if obj.languages else [],
               "api": utils.loads(obj.integrated_api) if obj.integrated_api else [],
               "create_at":utils.local_datetime_to_str(obj.create_at),
               "category": {"id": obj.category_id, 
                            "name": utils.lang_map_name(cate.name, cate.ename, lang),
                            "parent_id": cate_parent.id, 
                            "parent_name": utils.lang_map_name(cate_parent.name, cate_parent.ename, lang)},
               "attachment": {"id": obj.attachment.id, 
                            "name": obj.attachment.name, 
                            "size": obj.attachment.size, 
                            "path": widget.attach(obj.attachment.path)} if obj.attachment_id else {},
               "id": obj.job_uuid,
               "team": {"id": obj.team.uuid, "name": obj.team.name, "logo": widget.logo(obj.team.logo)},
               "last_view_time": utils.local_datetime_to_str(obj.last_view_time),
               "status": obj.status,
    }

    if obj.paymethod == "hour":
        res_job["hourly_range"] = _hourly_range[obj.level]

    is_favorite, p_detail = False, {"status": "", "proposal": 0, "interview": 0, "proposal_id": "", "contract_id": ""}
    proposal = Proposal.select().where(Proposal.job == obj.id)
    if user and user.identify[0] == "f":
        # 是否被开发者收藏
        favorite = Favorite.select().where(Favorite.user == user, Favorite.ftype == "DEV", Favorite.target_id == obj.id)
        if favorite.count() > 0:
            is_favorite = True

        # 该项目该开发者投标情况
        # 投标/邀标被拒绝之后，不允许在投标
        p = proposal.where(Proposal.user == user)
        # 开发者撤消或者开发者拒绝，需求者拒绝都不允许开发者投标
        sql_p1 = ((Proposal.status << ["active", "interview", "archive", "refuse"]) | ((Proposal.ptype == "D") & (Proposal.status == "revoke")))
        p1 = p.where(sql_p1).first()
        # 需求方offer允许发送多次
        p2 = p.where(Proposal.status == "hire").join(Contract).where(Contract.status.not_in(["unpaid", "revoke"])).first()

        p_status = p1 or p2
        if p_status: 
            p_detail["status"] = p_status.status
            p_detail["proposal_id"] = p_status.id
            p_detail["contract_id"] = p_status.contract.uuid if p_status.contract_id else ""

    res_job["proposal_user"] = list()
    if user and user.identify != "":
        # 需求方查询申请中人项目列表
        sql_going = ((Proposal.job == obj) & ((Proposal.status == "interview") | ((Proposal.status == "active") & (Proposal.ptype == "D")))) 
        proposal_going = Proposal.select().where(sql_going)
        for p in proposal_going:
            profile = p.user.profile.first()
            res_job["proposal_user"].append({
                "name": profile.name, 
                "user_id": p.user.uuid,
                "create_at": utils.local_datetime_to_str(p.update_at),
                "price": p.price,
            })

    # 报名人数
    p_detail["proposal"] = proposal.distinct(Proposal.user).count()
    p_detail["interview"] = proposal.where(Proposal.status.in_(["interview", "refuse", "hire"])).count()

    res_job["favorite"] = is_favorite
    res_job["proposal"] = p_detail

    # 该项目需求者发布其它项目情况
    other_jobs = Job.select(Job.name, Job.job_uuid, Job.paymethod).where(Job.team == obj.team, Job.status == "normal", Job.id != obj.id)
    out = []
    for x in other_jobs:
        out.append({"name":x.name, "paymethod":x.paymethod, "id":x.job_uuid})

    return {"error_code":0, "msg":"ok", "other":out, "job":res_job}

def get_job_list(user, params, lang):
    job_id = params.get("job_id")

    if job_id:
        return get_job(job_id, user, lang)

    pagesize = params.get("pagesize", "10")
    pagenum = params.get("pagenum", "1")
    if not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20111, "msg":"pagenation invalid"}

    pagesize = int(pagesize)
    pagenum = int(pagenum)
    if pagesize > 100:
        return {"error_code": 20112, "msg":"pagesize must less than 100"}

    if user and user.identify[0] != "f":
        qs = (Job.status << ("normal", "private"))
    else:
        qs = (Job.status == "normal")
    
    jobs = Job.select().where(qs)
    count = jobs.count()
    jobs = jobs.order_by(Job.create_at.desc()).paginate(pagenum, pagesize)
    out = []
    stats_dic = {}
    for obj in jobs:
        job = {"name": obj.name, 
               "description":obj.summary,
               "duration":obj.duration,
               "skills":utils.loads(obj.skills) if obj.skills else [],
               "workload":obj.workload, "paymethod":obj.paymethod,
               "budget":obj.budget, "level":obj.level,
               "create_at":utils.local_datetime_to_str(obj.create_at),
               "category": widget.get_category(obj.category_id).name,
               "eveluate_num": 0,
               "aver_score": 0,
               "favorite": False,
               "id":obj.job_uuid}

        if obj.team_id not in stats_dic:
            score = TeamStatistics.select(TeamStatistics.eveluate_num, 
                                        TeamStatistics.aver_score).where(TeamStatistics.user == obj.user, 
                                        TeamStatistics.team == obj.team).first()
            stats_dic[obj.team_id] = score
        else:
            if stats_dic[obj.team_id]:
                job["eveluate_num"] = stats_dic[obj.team_id].eveluate_num
                job["aver_score"] = stats_dic[obj.team_id].aver_score

        if user and user.identify[0] == "f":
            favorite = Favorite.select(Favorite.id).where(Favorite.user == user, 
                                Favorite.team == 0, Favorite.ftype == "DEV", 
                                Favorite.target_id == obj.id).first()
            if favorite:
                job["favorite"] = True
        out.append(job)
    return {"error_code":0, "msg":"ok", "jobs":out, "pagenum":pagenum, "count":count}


def job_proposal(user, params, lang):
    """ 查询项目及相应的申请人及合同情况"""
    jobs = Job.select().where(Job.user == user, Job.team == user.identify[1:]).order_by(Job.create_at.desc())
    job_draft, job_normal = [], []
    for job in jobs:
        tmp = {}
        tmp["id"] = job.job_uuid
        tmp["name"] = job.name
        tmp["description"] = job.summary
        tmp["category"] = widget.get_category(job.category_id).name
        tmp["paymethod"] = job.paymethod
        tmp["created_at"] = utils.local_datetime_to_str(job.create_at)
        tmp["status"] = job.status
        if job.status in ("normal", "private"):
            # TODO 全部查出，再过滤
            proposals = Proposal.select().where(Proposal.invite == user, Proposal.team == user.identify[1:], Proposal.job == job)
            tmp["apply_num"] = proposals.where(Proposal.status == "active", Proposal.ptype == "D", Proposal.archive_c == False).count()
            tmp["apply_new"] = proposals.where(Proposal.status == "active", Proposal.ptype == "D", Proposal.is_view == False).count()
            tmp["interview_num"] = proposals.where(Proposal.status == "interview", Proposal.archive_c == False).count()
            tmp["invite_num"] = proposals.where(Proposal.status == "active", Proposal.ptype == "I", Proposal.archive_c == False).count()
            tmp["contract_num"] = proposals.join(Contract, 
                                on=(Proposal.contract == Contract.id)).where(Proposal.archive_c == False, 
                                Proposal.status == "hire", Contract.status.not_in(["expire", "revoke", "refuse"])).count()
            job_normal.append(tmp)
        elif job.status == "draft":
            job_draft.append(tmp)

    return {"error_code": 0, "msg": "ok", "jobs": job_normal, "draft":job_draft}


def job_status_update(user, params):
    """
    草稿：公开、删除
    公开：私有、关闭
    私有：公开、关闭
    关闭：end
    """
    job_id = params.get("job_id")
    status = params.get("status")
    if not job_id or not status:
        return {"error_code": 20451, "msg": "params not enought"}
        
    if status not in ("normal", "private", "close", "delete"):
        return {"error_code": 20452, "msg": "status invalid"}

    job = Job.select().where(Job.job_uuid == job_id, Job.user == user, Job.team == int(user.identify[1:])).first()
    if not job:
        return {"error_code": 20453, "msg": "job exists"}

    if status == "normal":
        if job.status not in ("draft", "private", "close"):
            return {"error_code": 20454, "msg": "job status not allow noraml"}
        job.status = "normal"
    elif status == "private":
        if job.status != "normal":
            return {"error_code": 20455, "msg": "job status not allow private"}
        job.status = "private"
    elif status == "close":
        if job.status not in ("normal", "private"):
            return {"error_code": 20456, "msg": "job status not allow close"}
        job.status = "close"
    elif status == "delete":
        if job.status == "delete":
            return {"error_code": 20457, "msg": "job status not allow delete"}
        job.status = "delete"
    
    job.save()
    queue.to_queue({"type": "job_status_change", "job_id": job.id, "team_id": job.team_id})
    return {"error_code": 0, "msg": "ok"}


# 查询推荐的开发者
def job_freelancer_recommand(user, params, lang):
    job_id = params.get("job_id")

    job = Job.select().where(Job.job_uuid == job_id).first()
    if not job:
        return {"error_code": 20581, "msg": "job exists"}

    team_id = int(user.identify[1:])
    ucs = UserCategory.select(UserCategory.user).join(User)\
            .where(UserCategory.category == job.category_id, 
                    User.status == "active", User.to_dev == True).limit(11)
    out = []
    for u in ucs:
        if u.user_id == user.id:
            continue

        profile = u.user.profile.first()
        obj = {"id":u.user.uuid, "name":profile.name, "avatar":widget.avatar(profile.avatar),
                    "skills":utils.loads(profile.skills) if profile.skills else [], "title":profile.title,
                    "hourly":profile.hourly, "overview":profile.overview}

        related = Favorite.select(Favorite.id).where(Favorite.team==team_id, Favorite.target_id==profile.user_id).first()
        if related:
            obj['favorite'] = True
        else:
            obj['favorite'] = False

        location = ''
        if profile.location_id:
            city = widget.get_location(profile.location_id)
            location = utils.lang_map_name(city.name, city.ename, lang)
            if city.parent_id:
                province = widget.get_location(city.parent_id)
                location = "%s, %s" % (utils.lang_map_name(province.name, province.ename, lang), location)

        obj['location'] = location
        proposal = Proposal.select(Proposal.id).where(Proposal.user == u.user, 
                            Proposal.invite==user, Proposal.job == job, Proposal.status == "active").first()
        if proposal:
            obj["invite"] = True
        else:
            obj["invite"] = False
        out.append(obj)

    return {"error_code":0, "msg":"ok", "users":out}

# 查询我的所有项目
def get_my_jobs(user, params):
    t = params.get("t", "")
    pagesize = params.get("pagesize", "20")
    pagenum = params.get("pagenum", "1")
    out = []
    if t == "basic":
        jobs = Job.select(Job.job_uuid, Job.name).where(Job.user==user, Job.team == user.identify[1:], Job.status == "normal")
        for obj in jobs:
            out.append({"id":obj.job_uuid, "name":obj.name})
        return {"error_code":0, "msg":"ok", "jobs":out}

    if not pagesize or not pagenum or not str(pagesize).isdigit() or not str(pagenum).isdigit():
        return {"error_code": 20071, "msg":"pagenation invalid"}
    pagesize, pagenum = int(pagesize), int(pagenum)

    status = params.get("status", "normal")
    qs = ((Job.user == user) & (Job.team == user.identify[1:]))
    if status == "all":
        pass
    elif status == "normal":
        qs = (qs & (Job.status << ("normal", "private")))
    else:
        qs = (qs & (Job.status == status))
    jobs = Job.select().where(qs)
    count = jobs.count()
    jobs = jobs.order_by(Job.create_at.desc()).paginate(pagenum, pagesize)
    for obj in jobs:
        job = {"name": obj.name, 
               "description":obj.summary,
               "duration":obj.duration,
               "skills":utils.loads(obj.skills) if obj.skills else [],
               "workload":obj.workload, "paymethod":obj.paymethod,
               "budget":obj.budget, "level":obj.level,
               "create_at":utils.local_datetime_to_str(obj.create_at),
               "category": widget.get_category(obj.category_id).name,
               "id":obj.job_uuid,
               "status": obj.status,
               "contract_num": Contract.select(Contract.user).where(Contract.job == obj, Contract.status.not_in(["paid", "revoke", "refuse"])).count(),
        }
        out.append(job)
    return {"error_code":0, "msg":"ok", "jobs":out, "count":count, "pagenum":pagenum}

def delete_job(user, params):
    job_id = params.get("job_id")

    job = Job.select().where(Job.job_uuid == job_id, Job.status!="delete").first()
    if not job or job.user != user:
        return {"error_code": 20851, "msg": "job not exists"}

    if job.status != "draft":
        return {"error_code": 20852, "msg": "job not exists"}

    job.delete_instance()
    return {"error_code":0, "msg":"ok"}
