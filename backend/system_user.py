#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import traceback
import time
import logging
from models.user import User, Profile, Party, UserCategory, UserLanguage, UserQuestion
from models.system import SystemUser
from models.address import Address
from models.category import Category
from models.team import Team, Member, TeamProfile
from models.session import Session
from models.question import Question
from models.margin import Margin
from models.notify import Notify
from models.statistics import TeamStatistics, UserStatistics
from models.job import Job
from models.guid import GUID
from models.favorite import Favorite
from backend.password import check_password, generate_password
from backend.sms import verify_code
from backend import misc, widget
from common import utils, validate, queue
from config.settings import database, all_skills, all_languages
from backend.verity import id_verify_remote

logger = logging.getLogger(__name__)


def generate_token():
    return utils.rand_str(24) + utils.md5(str(utils.now()))[8:24]

def get(uname):
    if not uname:
        return {"error_code":20001, "msg":"parameters required"}
    user = SystemUser.select().where(SystemUser.username == uname).first()
    if not user:
        return {"error_code":20002, "msg":"user not exists"}
    res = {"error_code":0, "msg":"ok"}
    res['user'] = user
    return res

def login(uname, password):
    if not uname or not password:
        return {"error_code":20001, "msg":"parameters required"}

    user = SystemUser.select().where(SystemUser.username == uname).first()
    if not user:
        return {"error_code":20002, "msg":"user not exists"}
    if not check_password(password, user.password, user.salt):
        return {"error_code":20003, "msg":"username or password invalid"}

    res = {"error_code":0, "msg":"ok"}
    res['session_token'] = generate_token()
    sess = Session()
    sess.user = user
    sess.session_key = res['session_token']

    sess.expire_at = utils.timedelta(utils.now(), days=1)
    res['expire_at'] = 0
    sess.save()

    return res


def register(params, device):
    rtype = params.get('rtype', None)
    name = params.get('name', None)
    phone = params.get('phone', None)
    password = params.get('password', None)
    vcode = params.get('vcode', None)
    uname = params.get('username', '')
    cname = params.get('cname', '')
    notice = params.get('notice', "true")

    if not phone or not password or not vcode or not name or not rtype or not notice or not rtype.isdigit():
        return {"error_code":20021, "msg":"parameters required"}

    rtype = int(rtype)
    if not validate.is_phone(phone):
        return {"error_code":20022, "msg":"phone invalid"}

    # freelancer: 1, client: 2, client_person: 3
    if rtype not in [1, 2, 3]:
        return {"error_code":20022, "msg":"user type invalid"}

    if rtype == 2 and not cname or len(cname) > 100:
        return {"error_code":20022, "msg":"user type invalid or cname too long"}

    if not validate.is_verify_code(vcode):
        return {"error_code":20024, "msg":"verify code invalid"}
    
    if User.select().where(User.phone == phone).first():
        return {"error_code":20025, "msg":"user is exists"}

    if rtype != 1:
        username = phone
    else:
        # freelancer do not use username, just use phone to register
        # username = uname
        username = phone
    
    if not utils.is_username(username):
        return {"error_code":20023, "msg":"username invalid"}

    if User.select().where(User.username == username).first():
        return {"error_code":20025, "msg":"user is exists"}

    res = verify_code(phone=phone, code=vcode)
    if res['error_code'] != 0:
        return res
    
    user_id = GUID.guid()
    team_id = GUID.guid()
    with database.atomic() as txn:
        try:
            pwd, salt = generate_password(password.encode('utf-8'))
            user = User()
            user.id = user_id
            user.username = username
            user.password = pwd
            user.salt = salt
            user.phone = phone
            #user.verifycode = vcode
            user.save(force_insert=True)

            profile = Profile()
            profile.user = user
            profile.name = name
            profile.avatar = widget.avatar()

            if notice == "true":
                profile.is_notice = True
            profile.save()

            party = Party()
            party.user = user
            party.vip = False
            party.connects = 60
            party.agency_connects = 60
            party.save()

            margin = Margin()
            margin.user = user
            margin.save()

            if rtype == 1:
                user.identify = 'f%s' % user.id
                user.app_identify = 'f%s' % user.id
                user.status = "unactive"
                user.to_dev = True
                user.to_req = False
                user.save()

                queue.to_queue({"type":"user_register", "user_id":user.id})
            else:
                team = Team()
                team.id = team_id
                team.user = user
                if rtype == 2:
                    team.name = cname
                else:
                    team.name = "个人需求方"
                team.team_type = 'client'
                team.status = "normal"
                team.logo = widget.logo()
                team.save(force_insert=True)

                team_profile = TeamProfile()
                team_profile.team = team
                team_profile.phone = phone
                team_profile.save()

                user.identify = 'c%s' % team.id
                user.app_identify = 'c%s' % team.id
                user.status = "active"
                user.to_req = True
                user.to_dev = False
                user.save()

                queue.to_queue({"type":"user_register", "user_id":user.id, "team_id":team.id})
        except Exception, e:
            logger.error(traceback.format_exc())
            txn.rollback()
            return {"error_code":20026, "msg":"signup error"}

    res = login(username, password, "false", device)
    return res


def password_reset(params):
    uname = params.get('username')
    password = params.get('password')
    vcode = params.get('vcode')
    if not uname or not password or not vcode:
        return {"error_code":20091, "msg":"parameters required"}

    if not validate.forget_password(username=uname, vcode=vcode):
        return {"error_code":20092, "msg":"verify code invalid"}

    user = User.select().where(User.username == uname or User.email == uname).first()
    if not user:
        return {"error_code":20093, "msg":"user not exists"}

    # verity code
    res = verify_code(phone=user.phone, code=vcode)
    if res['error_code'] != 0:
        return res

    pw, salt = generate_password(password)
    user.password = pw
    user.salt = salt
    user.update_at = utils.now()
    user.save()
    return {"error_code":0, "msg":"ok"}


def password_change(user, params):
    password_old = params.get("password_old")
    password = params.get("password")
    if not password_old or not password:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if not validate.is_password(password_old) or not validate.is_password(password):
        return {"error_code": 80003, "msg": "parameters illegal"}

    if not check_password(password_old, user.password, user.salt):
        return {"error_code": 20094, "msg": "password invalid"}

    pw, salt = generate_password(password)
    user.password = pw
    user.salt = salt
    user.update_at = utils.now()
    user.save()
    
    queue.to_queue({"type":"user_password_change", "user_id":user.id, 
        "team_id": user.identify[1:] if user.identify[0] != "f" else None})
    return logout(user)

def user_all_info(cls):
    return;
    if cls.user:
        cls.user.profile.avatar = widget.avatar(cls.user.profile.avatar)
        teams = Team.select(Team.id, Team.name, Team.uuid, Team.logo).where(Team.user == cls.user, Team.status=="normal")
        cls.user.current_team = None
        for x in teams:
            x.logo = widget.logo(x.logo)
            if x.id == int(cls.user.identify[1:]):
                cls.user.current_team = x
        cls.user.team = teams

def logout(user):
    if user:
        Session.delete().where(Session.user==user)
    return {"error_code":0, "msg":"ok"}

def category_create(user, params):
    result = category_update(user, params)
    if not result['error_code']:
        user.reg_step = "category"
        user.save()
    return result

def category_update(user, params):
    # category example: 1,2,3,4,5
    category = params.get('category')
    try:
        category_list = set(category.split(","))
    except:
        return {"error_code":20101, "msg":"category invalid"}

    if len(category_list) != len(filter(utils.safe_id, category_list)):
        return {"error_code":20103, "msg":"category invalid"}

    if len(category_list) == 0:
        return {"error_code":20102, "msg":"category not empty"}

    cates = Category.select(Category.id)
    cates = set([str(x.id) for x in cates])
    if not category_list <= cates:
        return {"error_code":20104, "msg":"category error"}
    if len(category_list) > 10:
        return {"error_code":20105, "msg":"category too large"}
    exist_list = UserCategory.select(UserCategory.category).where(UserCategory.user == user)
    exist_list = set([str(x.category_id) for x in exist_list])
    if category_list == exist_list:
        return {"error_code":0, "msg":"ok"}
    new_cates = list(category_list.difference(exist_list))
    del_cates = list(exist_list.difference(category_list))
    for c in new_cates:
        tmp_cate = UserCategory()
        tmp_cate.user = user
        tmp_cate.category = c
        tmp_cate.save()

    for d in del_cates:
        UserCategory.delete().where(UserCategory.user == user, UserCategory.category == d).execute()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["category", ]})
    return {"error_code":0, "msg":"ok"}

def get_category(user, lang="zh_CN"):
    cates = UserCategory.select().join(Category).where(UserCategory.user == user)
    cate_arr = []
    if lang == "zh_CN":
        for x in cates:
            cate_arr.append({
                "name": x.category.name, "category_id": x.category.id,
                "parent_name": x.category.parent.name, "parent_id": x.category.parent.id})
    else:
        for x in cates:
            cate_arr.append({
                "name": x.category.ename, "category_id": x.category.id,
                "parent_name": x.category.parent.ename, "parent_id": x.category.parent.id})
    return {"error_code": 0, "msg": "ok", "categorys": cate_arr}

#创建个人资料
def profile_create(user, params):
    title = params.get("title", "").strip()
    overview = params.get("intro", "").strip()
    email = params.get("email", "").strip()
    skills = params.get("skills", "").strip()
    english = params.get("english", "").strip()
    other = params.get("other", "").strip()
    workload = params.get("workload", "").strip()

    if not title or not overview or not email or not skills or not english or not workload:
        return {"error_code":20121, "msg":"parameters not enough"}
    if len(title) > 29:
        return {"error_code":20122, "msg":"title too long"}

    if len(overview) > 1024 * 1024 * 4:
        return {"error_code":20123, "msg":"overview too long"}

    if not validate.is_email(email):
        return {"error_code":20124, "msg":"email invalid"}
    if not workload.isdigit():
        return {"error_code":20125, "msg":"workload invalid"}
    workload = int(workload)
    if not 1<= workload <= 3:
        return {"error_code":20125, "msg":"workload must between 1-3"}

    if english not in ("1", "2", "3", "4"):
        return {"error_code":20126, "msg":"english level invalid"}

    s = None
    try:
        s = [x for x in skills.split(",") if x in all_skills]
    except:
        return {"error_code":20127, "msg":"skills invalid"}

    other_lan = None
    if other:
        try:
            other_lan = utils.loads(other)
            for y in other_lan:
                if y not in all_languages or other_lan[y] not in ("1", "2", "3", "4"):
                    other_lan.pop(y)
        except:
            return {"error_code":20128, "msg":"other language invalid"}

    # 添加时不娇艳邮箱是否已经绑定
    #u = User.select().where(User.email == email).first()
    #if u and u.id != user.id:
    #    return {"error_code":20129, "msg":"user is exists"}

    with database.atomic() as txn:
        try:
            user.email = email
            user.reg_step = "profile"
            user.save()

            profile = user.profile.first()
            profile.title = title
            profile.overview = overview
            profile.english = english
            profile.workload = workload
            if s:
                profile.skills = utils.dumps(s)
            profile.save()

            if other_lan:
                for x in other_lan:
                    ul = UserLanguage.select().where(UserLanguage.user==user,UserLanguage.name==x).first()
                    if ul and ul.level != other_lan[x]:
                        ul.level = other_lan[x]
                        ul.save()
                    elif not ul:
                        UserLanguage.create(user=user, name=x, level=other_lan[x])
        except Exception, e:
            txn.rollback()
            return {"error_code":20129, "msg":"update error"}
    return {"error_code":0, "msg":"ok"}

def profile_resume(user, params):
    level = params.get('level')
    if not level:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if level not in ("entry", "middle", "expert"):
        return {"error_code": 20016, "msg": "level invalid"}

    profile = user.profile.first()
    if not profile:
        return {"error_code":20002, "msg":"user not exists"}

    user.reg_step = 'resume'
    user.save()

    profile.level = level
    profile.save()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["level", ]})
    return {"error_code": 0, "msg": "ok"}

def other_create(user, params):
    amount = utils.decimal_two(params.get("amount", ""))
    location = utils.safe_id(params.get("location", ""))
    address = params.get("address", "")
    postcode = params.get("postcode", "")

    if not location or not amount:
        return {"error_code": 80002, "msg": "not enough parameters"}

    add = Address.select().where(Address.id == location).first()
    if not add or add and add.level != 3:
        return {"error_code": 20167, "msg": "location invalid"}

    if postcode and len(postcode) > 20 or len(address) > 100:
        return {"error_code": 20162, "msg": "too long"}

    if not amount:
        return {"error_code": 20163, "msg": "hourly invalid"}

    with database.atomic() as txn:
        try:
            user.reg_step = "other"
            user.status = "active"
            user.save()

            # 任务加分字断
            columns = ["hourly", "location", "address"]

            profile = user.profile.first()
            profile.hourly = amount
            profile.location = location
            profile.address = address
            if postcode: 
                profile.postcode = postcode
                columns.append("postcode")
            profile.save()
            queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": columns})
        except:
            return {"error_code":20164, "msg":"save error"}
    return {"error_code": 0, "msg": "ok"}

def reg_complete(user, params):
    status = params.get("status", "")
    if status not in ("draft", "audit"):
        return {"error_code":20181, "msg":"status invalid"}

    user.reg_step = "draft"
    user.save()
    # TODO 注册完成后的一系列操作
    return {"error_code":0, "msg":"ok"}

def user_question(user):
    question = UserQuestion.select().join(Question).where(UserQuestion.user == user).first()
    if not question:
        return {"error_code": 20241, "msg": "user unset protect question"}

    out = [dict(
        question_id=question.question.id,
        name=question.question.name,
        ename=question.question.ename,
        answer=question.answer,
    )]
    return {"error_code": 0, "msg": "ok", "questions": out}


def question_create(user, params):
    question_id = utils.safe_id(params.get("question_id"))
    answer = params.get("answer")
    if not question_id or not answer:
        return {"error_code": 80002, "msg": "no enough parameters"}

    question = Question.select().where(Question.id == question_id).first()
    if not question:
        return {"error_code": 20242, "msg": "protect question not exists"}

    uq = UserQuestion.select().where(UserQuestion.user == user).first()
    if uq:
        return {"error_code": 20243, "msg": "password question already exists"}

    u = UserQuestion()
    u.user = user
    u.question = question
    u.answer = answer
    u.save()

    queue.to_queue({"type":"user_question_create", "user_id":user.id,
        "team_id": user.identify[1:] if user.identify[0] != "f" else None})
    return {"error_code": 0, "msg": "ok"}


def question_update(user, params):
    question_id = utils.safe_id(params.get('question_id'))
    answer_old = params.get('answer_old')
    answer = params.get('answer')

    if not question_id or not answer_old or not answer:
        return {"error_code": 80002, "msg": "no enough parameters"}

    question = Question.select().where(Question.id == question_id).first()
    if not question:
        return {"error_code": 20242, "msg": "protect question not exists"}

    uq = UserQuestion.select().where(UserQuestion.user == user).first()
    if not uq:
        return {"error_code": 20241, "msg": "user protect question not exists"}

    if uq.answer != answer_old:
        return {"error_code": 20244, "msg": "error answer"}

    uq.question = question_id
    uq.answer = answer
    uq.create_at = utils.now()
    uq.save()
    return {"error_code": 0, "msg": "ok"}


def user_profile(user, params, lang):
    origin_user = user
    uuid = params.get("uuid", "")
    if uuid:
        user = User.select().where(User.uuid == uuid).first()
        if not user:
            return {"error_code": 20002, "msg": "user not exist"}

    profile = user.profile.first()
    languages = []
    ul = UserLanguage.select().where(UserLanguage.user == user)
    for u in ul:
        languages.append(dict(
            language_id=u.id,
            name=u.name,
            level=u.level,
        ))
    out = dict()
    # user self can get private information
    if not uuid:
        out["reg_step"] = user.reg_step
        out["id_number"] = "%s********%s" % (profile.id_number[:6], profile.id_number[14:]) if profile.id_number else ""
        out["alipay"] = profile.alipay
        out["email"] = user.email
        out["phone"] = user.phone

    out["name"] = profile.name
    out["username"] = user.username
    out["avatar"] = widget.avatar(profile.avatar)
    out["completeness"] = profile.completeness
    out["visibility"] = profile.visibility
    out["level"] = profile.level
    out["title"] = profile.title
    out["overview"] = profile.overview
    out["hourly"] = profile.hourly
    out["english"] = profile.english
    out["skills"] = utils.loads(profile.skills) if profile.skills else []
    out["available"] = profile.available
    out["workload"] = profile.workload
    location = {}
    if profile.location_id:
        city = widget.get_location(profile.location_id)
        province = widget.get_location(city.parent_id)

        location["location_id"] = profile.location_id
        location["name"] = utils.lang_map_name(city.name, city.ename, lang)
        location["parent_id"] = province.id
        location["parent_name"] = utils.lang_map_name(province.name, province.ename, lang)
    out["location"] = location
    out["address"] = profile.address
    out["postcode"] = profile.postcode
    out['id'] = user.uuid
    out["languages"] = languages
    out["imid"] = user.id
    if uuid:
        favorites = Favorite.select().where(Favorite.user==origin_user, Favorite.target_id==profile.user_id, Favorite.ftype == 'REQ').first()
        if favorites:
            out["favorite"] = True
        else:
            out["favorite"] = False
    # 开发者的评价数量和平均得分
    score = UserStatistics.select(UserStatistics.eveluate_num, UserStatistics.aver_score).where(UserStatistics.user == user).first()
    out["eveluate_num"] = score.eveluate_num if score else 0
    out["aver_score"] = score.aver_score if score else 0
    return {"error_code": 0, "msg": "ok", "profile": out}


def user_profile_update(user, params):
    if len(params) == 0:
        return {"error_code": 0, "msg": "ok"}

    email = params.get("email")
    name = params.get("name")
    location = utils.safe_id(params.get('location'))
    address = params.get("address")
    postcode = params.get("postcode")
    available = params.get("available")
    workload = params.get("workload")
    title = params.get("title")
    overview = params.get("overview")
    hourly = params.get("hourly")
    skills = params.get("skills")
    english = params.get("english")
    other = params.get("other", "").strip()
    level = params.get("level")
    
    # 更新分值字断名称
    columns = list() 

    profile = user.profile.first()
    if email is not None:
        if not validate.is_email(email):
            return {"error_code": 202710, "msg": "email invalid"}
        u = User.select().where(User.email == email).first()
        if u and u.id != user.id:
            return {"error_code": 202711, "msg": "email is exists"}

        user.email = email
        user.save()
        columns.append("email")

    if level is not None:
        if level not in ("entry", "middle", "expert"):
            return {"error_code": 202712, "msg": "level invalid"}
        if profile.level != level:
            profile.level = level
            columns.append("level")

    if name is not None:
        if name.strip() != profile.name:
            if profile.id_number:
                return {"error_code": 20271, "msg": "already verify user, not allow modify name"}
        profile.name = name

    if location:
        add = Address.select().where(Address.id == location).first()
        if not add or add and add.level != 3:
            return {"error_code": 20272, "msg": "location invalid"}
        profile.location = location
        columns.append("location")

    if address is not None:
        if len(address) > 100:
            return {"error_code": 20273, "msg": "address too long"}
        profile.address = address
        columns.append("address")

    if postcode is not None:
        if len(postcode) > 20:
            return {"error_code": 20274, "msg": "postcode too long"}
        profile.postcode = postcode
        columns.append("postcode")

    if available is not None:
        if available == "true":
            profile.available = True
        elif available == "false":
            profile.available = False

    if workload is not None:
        if not (workload.isdigit() and 1 <= int(workload) <= 3):
            return {"error_code": 202713, "msg": "workload invalid"}
        profile.workload = workload
        columns.append("workload")

    if title is not None:
        if len(title) > 29:
            return {"error_code": 20275, "msg": "title too long"}
        profile.title = title
        columns.append("title")

    if overview is not None:
        if len(overview) > 1024 * 1024 * 4:
            return {"error_code": 20276, "msg": "overview too long"}
        profile.overview = overview
        columns.append("overview")

    if hourly is not None:
        try:
            hourly = float(hourly)
        except:
            return {"error_code": 20277, "msg": "hourly invalid"}
        profile.hourly = hourly
        columns.append("hourly")

    if english is not None:
        if english not in ("1", "2", "3", "4"):
            return {"error_code": 20278, "msg": "english level invalid"}
        profile.english = english
        columns.append("english")

    other_lan = None
    if other:
        try:
            other_lan = utils.loads(other)
            for y in other_lan:
                if y not in all_languages or str(other_lan[y]) not in ("1", "2", "3", "4"):
                    other_lan.pop(y)
        except:
            return {"error_code":20128, "msg":"other language invalid"}

    if other_lan != None:
        _user_lang = UserLanguage.select().where(UserLanguage.user==user)
        for x in _user_lang:
            if x.name not in other_lan:
                x.delete_instance()
            else:
                if x.level != other_lan[x.name]:
                    x.level = other_lan[x.name]
                    x.save()
                    other_lan.pop(x.name)
                else:
                    other_lan.pop(x.name)

        for y in other_lan:
            UserLanguage.create(user=user, name=y, level=other_lan[y])
        columns.append("other_language")

    if skills is not None:
        s = None
        try:
            s = [x for x in skills.split(",") if x in all_skills]
        except:
            return {"error_code": 20279, "msg": "skills invalid"}
        if s:
            profile.skills = utils.dumps(s)
            columns.append("skills")

    profile.save()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": columns})
    return {"error_code": 0, "msg": "ok"}

def create_client(user, params):
    name = params.get("name", "")
    if not name or len(name) > 30:
        return {"error_code":20251, "msg":"name invalid"}

    #team = Team.select().where(Team.user == user, Team.name == name).first()
    team = Team.select().where(Team.user == user).first()
    if team:
        return {"error_code":20252, "msg":"team is exists and must one"}

    team_id = GUID.guid()
    team = Team()
    team.id = team_id
    team.user = user
    team.name = name
    team.status = "normal"
    team.team_type = 'client'
    team.logo = widget.logo()
    team.save(force_insert=True)

    user.to_req = True
    user.identify = "c%s" % team.id
    user.save()

    team_profile = TeamProfile()
    team_profile.team = team
    team_profile.save()

    #Member.create(user=user, team=team, mtype='owner')
    return {"error_code":0, "msg":"ok"}

# 创建开发者身份
def create_freelancer(user):
    if user.to_dev:
        return {"error_code": 0, "msg":"ok"}

    user.to_dev = True
    # 引导到入口页面
    #user.reg_step = "category"
    user.status = "unactive"
    user.identify = "f%s" % user.id
    user.save()
    return {"error_code": 0, "msg":"ok"}

def client_info(params, lang):
    team_id = params.get("team_id", "")
    if not team_id:
        return {"error_code":20321, "msg":"paramsmeter invalid"}
    team = Team.select().where(Team.uuid == team_id).first()
    if not team:
        return {"error_code":20322, "msg":"client not exists"}

    statis = TeamStatistics.select().where(TeamStatistics.team == team).first()
    if statis:
        info = {"eveluate_num":statis.eveluate_num, "total_amount":statis.total_amount,
                "hours":statis.hours, "jobs":statis.jobs, "hires":statis.hires,
                "open_jobs":statis.open_jobs, "score":statis.score, "aver_score": statis.aver_score}
    else:
        info = {"eveluate_num":0, "total_amount":0,
                "hours":0, "jobs":0, "hires":0,
                "open_jobs":0, "score":0, "aver_score": 0}

    info.update({"name":team.name, "reg_at":utils.local_datetime_to_str(team.create_at), "location":""})
    if team.location_id:
        city = widget.get_location(team.location_id)
        info['location'] = utils.lang_map_name(city.name, city.ename, lang)
        if city.parent_id:
            province = widget.get_location(city.parent_id)
            info['location'] += ",%s" % utils.lang_map_name(province.name, province.ename, lang)
    return {"error_code":0, "msg":"ok", "info":info}


def identification(user, params):
    name = params.get("name")
    id_number = params.get("id_number")

    if not name or not id_number:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if not 15 <= len(id_number) <= 18 or not id_number[:-1].isdigit():
        return {"error_code": 80002, "msg": "id_number invalid"}

    profile = user.profile.first()
    # verify user record into profile table
    if profile.id_number:
        return {"error_code": 20262, "msg": "already verify"}

    tmp = Profile.select().where(Profile.id_number == id_number).first()
    if tmp:
        return {"error_code": 20262, "msg": "already verify"}

    key, value = misc.generate_verify_init_data(user, "id_number")
    m = misc.misc_get_or_create(key=key, value=value)
    misc_value = utils.loads(m.value)
    if misc_value['id_verify_count'] >= 3:
        return {"error_code": 20263, "msg": "verify too many times"}

    # verify remote
    try:
        is_verify = id_verify_remote(name, id_number)
    except:
        return {"error_code": 20264, "msg": "verify failed"}

    if not is_verify:
        misc_value['id_verify_count'] += 1
        misc_value['last_verify_time'] = utils.now()
        misc.misc_update(key, misc_value)
        return {"error_code": 20264, "msg": "verify failed"}
    else:
        misc.misc_delete(key)
        profile.name = name
        profile.id_number = id_number
        profile.save()
        team_id = user.identify[1:] if user.identify[0] != "f" else None
        queue.to_queue({"type": "user_identify", "user_id": user.id, "team_id": team_id})
        return {"error_code": 0, "msg": "ok"}

def change_role(user, uuid, change_to_role):
    if change_to_role == "f":
        if user.identify[0] != "f":
            user.identify = "f%s" % user.id
            user.save()
        else:
            return False
    else:
        team = Team.select().where(Team.user == user, Team.uuid == uuid).first()
        if team:
            #if user.status == "unactive":
            #    user.status = "active"
            identify = "c%s" % team.id
            if user.identify != identify:
                user.identify = identify
                user.save()
        else:
            return False
    return True

def user_role_list(user):
    profile = user.profile.first()

    teams = Team.select().where(Team.user == user)
    out = []
    for team in teams:
        out.append({"name":team.name, "team_id":team.uuid})

    return {"error_code": 0, "msg": "ok", "teams": out, "name":profile.name, "id":user.uuid}

def get_user_by_uuid(uuid):
    user = User.select().where(User.uuid==uuid).first()
    if not user:
        return None
    profile = user.profile.first()
    profile.avatar = widget.avatar(profile.avatar)
    user.profile = profile
    return user

def user_role_change(user, params, token, device):
    uid = params.get("id", "")
    if device == "web":
        role, role_id = user.identify[0], int(user.identify[1:])
    else:
        role, role_id = user.app_identify[0], int(user.app_identify[1:])

    tmp_user = User.select().where(User.uuid==uid).first()
    identify = None
    if not tmp_user:
        tmp_team = Team.select().where(Team.uuid==uid).first()
        if not tmp_team or tmp_team.user != user:
            return {"error_code": 20332, "msg": "the role not change, not allowed"}
        if role == "f":
            identify = "c%s" % tmp_team.id
    else:
        if tmp_user.id != user.id:
            return {"error_code": 20332, "msg": "the role not change, not allowed"}
        if role == "c":
            identify = "f%s" % tmp_user.id

    if identify:
        if device == "web":
            user.identify = identify
            user.save()
        else:
            user.app_identify = identify
            user.save()

    if device in ("ios", "android"):
        qs = Session.delete().where(Session.user==user, Session.session_key!=token, Session.device << ("ios", "android"))
        qs.execute()
    return {"error_code": 0, "msg": "ok"}


def alipay_create(user, params):
    alipay = params.get("alipay", "").strip()

    if not alipay:
        return {"error_code": 20481, "msg": "params not enough"}

    profile = user.profile.first()
    if profile.alipay:
        return {"error_code": 20482, "msg": "alipay already exists"}

    profile.alipay = alipay
    profile.save()
    return {"error_code": 0, "msg": "ok"}


def alipay_delete(user, params):
    profile = user.profile.first()
    if not profile:
        return {"error_code": 20486, "msg": "alipay not exists"}

    profile.alipay = ""
    profile.save()
    return {"error_code": 0, "msg": "ok"}


def password_verify(user, params):
    password = params.get("password")
    if not check_password(password, user.password, user.salt):
        return {"error_code": 20391, "msg": "password invalid"}

    user.last_verify = utils.now()
    user.save()
    return {"error_code": 0, "msg": "ok"}

def im_session_verify(params):
    token = params.get("session_token")
    session = Session.select().where(Session.session_key==token, Session.expire_at>utils.now()).first()
    if not session:
        return {"error_code":1, "msg":"token not exist"}
    user = session.user
    role, tid = user.app_identify[0], int(user.app_identify[1:])
    if role == "f":
        return {"error_code":0, "msg":"ok", "id":user.id}
    team = Team.select().where(Team.id == tid).first()
    if not team:
        return {"error_code":1, "msg":"token error"}
    return {"error_code":0, "msg":"ok", "id":team.id}

def get_jump_code(user):
    import uuid
    code = str(uuid.uuid4())
    key = "jump-%s" % code
    value = {"expire_at":utils.stamp()+600, "user_id":user.id}
    obj = misc.misc_get(key)
    if not obj:
        misc.misc_create(key, value)
    else:
        misc.misc_update(key, value, obj)
    return {"error_code":0, "msg":"ok", "code":code}

def client_login(params):
    code = params.get("code")
    if not code or len(code) != 36:
        return {"error_code":1, "msg":"params invalid"}
    key = "jump-%s" % code
    obj = misc.misc_get(key)
    if not obj:
        return {"error_code":1, "msg":"code not exists"}
    dic = utils.loads(obj.value)

    obj.delete_instance()
    if dic['expire_at'] < utils.stamp():
        return {"error_code":1, "msg":"code expire"}

    user = User.select().where(User.id==dic['user_id']).first()
    res = {"error_code":0, "msg":"ok"}
    res['session_token'] = generate_token()
    sess = Session()
    sess.user = user
    sess.session_key = res['session_token']
    sess.expire_at = utils.timedelta(utils.now(), days=1)
    res['expire_at'] = 0
    sess.save()
    res['identify'] = user.identify
    return res
