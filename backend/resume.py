#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from common import utils, queue
from models.attachment import Attachment
from models.address import Address
from models.resume import Employment, Education, Portfolio
from models.user import User
from backend import widget


def employment_list(user, params, lang):
    # user_id means query other freealncer employment info
    user_id = params.get("user_id")
    if user_id:
       user = User.select().where(User.uuid == user_id).first() 
       if not user:
           return {"error_code": 20135, "msg": "user_id invlid"}
       
    eid = params.get('eid')
    if eid is None:
        employments = Employment.select().where(Employment.user == user)
    else:
        eid = utils.safe_id(eid)
        if not eid:
            return {"error_code": 80003, "msg": "parameters illegal"}
        employments = Employment.select().where(Employment.user == user, Employment.id == eid)

    emp = list()
    for employment in employments:
        tmp = dict()
        tmp["id"] = employment.id
        tmp["company"] = employment.company
        city = widget.get_location(employment.city_id)
        province = widget.get_location(city.parent_id)
        tmp["city"] = {
            "id": city.id, 
            "name": utils.lang_map_name(city.name, city.ename, lang),
            "parent_id": province.id,
            "parent_name": utils.lang_map_name(province.name, province.ename, lang)}
        tmp["title"] = employment.title
        tmp["role"] = employment.role
        tmp["start_at"] = utils.local_datetime_to_str(employment.start_at)
        tmp["end_at"] = utils.local_datetime_to_str(employment.end_at)
        tmp["working"] = employment.working
        tmp["detail"] = employment.detail
        emp.append(tmp)
    result = {"error_code": 0, "msg": "ok"}
    result.update({"employments": emp})
    return result


def employment_add(user, params):
    company = params.get('company')
    city_id = utils.safe_id(params.get('city_id'))
    title = params.get('title')
    role = utils.safe_id(params.get('role'))
    start_at = utils.str_to_datetime(params.get('start_at'), pattern='%Y-%m', utc=False)
    end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y-%m', utc=False)
    working = params.get('working')
    detail = params.get('detail', '')

    if not company or not city_id or not title or not start_at or not end_at or not working or not role:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(company)) > 100:
        return {"error_code": 20132, "msg": "company or country too long"}

    if role not in xrange(1, 6):
        return {"error_code": 20133, "msg": "role selected not right"}

    add = Address.select().where(Address.id == city_id).first()
    if not add or add and add.level != 3:
        return {"error_code": 20134, "msg": "city invalid"}

    employment = Employment()
    employment.user = user
    employment.company = company
    employment.city = city_id
    employment.title = title
    employment.role = role
    employment.start_at = start_at
    employment.end_at = end_at
    if working == 'true':
        employment.working = True
    if detail:
        employment.detail = detail
    employment.save()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["employment",]})
    return {"error_code": 0, "msg": "ok", "employment_id": employment.id}

def employment_change(user, params):
    eid = utils.safe_id(params.get('eid'))
    company = params.get('company')
    city_id = utils.safe_id(params.get('city_id'))
    title = params.get('title')
    role = utils.safe_id(params.get('role'))
    start_at = utils.str_to_datetime(params.get('start_at'), pattern='%Y-%m', utc=False)
    end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y-%m', utc=False)
    working = params.get('working')
    detail = params.get('detail', '')

    if not eid or not company or not city_id or not title or not start_at or not end_at or not working or not role:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(company)) > 100:
        return {"error_code": 20132, "msg": "companytoo long"}

    if role not in xrange(1, 6):
        return {"error_code": 20133, "msg": "role selected not right"}

    add = Address.select().where(Address.id == city_id).first()
    if not add or add and add.level != 3:
        return {"error_code": 20134, "msg": "city invalid"}

    employment = Employment.select().where(Employment.user == user, Employment.id == eid).first()
    if not employment:
        return {"error_code": 20131, "msg": "employment not exists"}

    employment.company = company
    employment.city = city_id
    employment.title = title
    employment.role = role
    employment.start_at = start_at.date()
    employment.end_at = end_at.date()
    employment.detail = detail
    if working == 'true':
        employment.working = True
    else:
        employment.working = False
    employment.update_at = utils.now()
    employment.save()
    return {"error_code": 0, "msg": "ok"}


def employment_remove(user, params):
    eid = utils.safe_id(params.get('eid'))
    if not eid:
        return {"error_code": 80002, "msg": "no enough parameters"}

    employment = Employment.delete().where(Employment.user == user, Employment.id == eid)
    if not employment:
        return {"error_code": 20131, "msg": "employment not exists"}

    employment.execute()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["employment",]})
    return {"error_code": 0, "msg": "ok"}


def education_list(user, params):
    # user_id means query other freealncer employment info
    user_id = params.get("user_id")
    if user_id:
       user = User.select().where(User.uuid == user_id).first() 
       if not user:
           return {"error_code": 20144, "msg": "user_id invalid"}

    eid = params.get('eid')
    if eid is None:
        education = Education.select().where(Education.user == user)
    else:
        eid = utils.safe_id(eid)
        if not eid:
            return {"error_code": 80003, "msg": "parameters illegal"}
        education = Education.select().where(Education.user == user, Education.id == eid)

    res = list()
    for edu in education:
        tmp = dict()
        tmp["id"] = edu.id
        tmp["start_at"] = utils.local_datetime_to_str(edu.start_at)
        tmp["end_at"] = utils.local_datetime_to_str(edu.end_at)
        tmp["school"] = edu.school
        tmp["degree"] = edu.degree
        tmp["area"] = edu.area
        tmp["detail"] = edu.detail
        res.append(tmp)

    return {"error_code": 0, "msg": "ok", "educations": res}


def education_add(user, params):
    start_at = utils.str_to_datetime(params.get('start_at'), pattern='%Y', utc=False)
    end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y', utc=False)
    school = params.get('school')
    degree = params.get('degree')
    area = params.get('area')
    detail = params.get('detail')
    if not start_at or not end_at or not school or not degree:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(school)) > 100:
        return {"error_code": 20141, "msg": "school name too long"}

    if degree not in ("senior", "college", "bachelor", "master", "mba", "emba",
                      "doctor", "others"):
        return {"error_code": 20143, "msg": "degree option not right"}

    education = Education()
    education.user = user
    education.start_at = start_at
    education.end_at = end_at
    education.school = school
    education.degree = degree
    if area:
        education.area = area
    if detail:
        education.detail = detail
    education.save()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["education",]})
    return {"error_code": 0, "msg": "ok", "education_id": education.id}

def education_change(user, params):
    eid = utils.safe_id(params.get('eid'))
    start_at = utils.str_to_datetime(params.get('start_at'), pattern='%Y', utc=False)
    end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y', utc=False)
    school = params.get('school')
    degree = params.get('degree')
    area = params.get('area')
    detail = params.get('detail')
    if not eid or not start_at or not end_at or not school or not degree or not area:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(school)) > 100:
        return {"error_code": 20141, "msg": "school name too long"}

    if degree not in ("senior", "college", "bachelor", "master", "mba", "emba",
                      "doctor", "others"):
        return {"error_code": 20143, "msg": "degree option not right"}

    education = Education.select().where(Education.user == user, Education.id == eid).first()
    if not education:
        return {"error_code": 20142, "msg": "education not exists"}

    education.start_at = start_at.date()
    education.end_at = end_at.date()
    education.school = school
    education.degree = degree
    education.area = area
    education.detail = detail
    education.update_at = utils.now()
    education.save()

    return {"error_code": 0, "msg": "ok"}

def education_remove(user, params):
    eid = utils.safe_id(params.get('eid'))
    if not eid:
        return {"error_code": 80002, "msg": "no enough parameters"}

    education = Education.delete().where(Education.user == user, Education.id == eid)
    if not education:
        return {"error_code": 20142, "msg": "education not exists"}

    education.execute()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["education",]})
    return {"error_code": 0, "msg": "ok"}

def portfolio_list(user, params):
    # user_id means query other freealncer employment info
    user_id = params.get("user_id")
    if user_id:
       user = User.select().where(User.uuid == user_id).first() 
       if not user:
           return {"error_code": 20154, "msg": "user_id invalid"}
    
    pid = params.get('pid')
    if pid is None:
        portfolio = Portfolio.select().where(Portfolio.user == user)
    else:
        pid = utils.safe_id(pid)
        if not pid:
            return {"error_code": 80003, "msg": "parameters illegal"}

        portfolio = Portfolio.select().where(Portfolio.user == user, Portfolio.id == pid)

    res = list()
    for por in portfolio:
        tmp = {}
        tmp["id"] = por.id
        tmp["name"] = por.name
        tmp["detail"] = por.detail
        cate = widget.get_category(por.category_id)
        cate_parent = widget.get_category(cate.parent_id)

        tmp["category"] = {"id": cate.id, "name": cate.name,
                           "parent_id": cate_parent.id,
                           "parent_name": cate_parent.name}
        if por.picture_id != 0:
            tmp["picture"] = {"id": por.picture_id, "name": por.picture.name,
                              "size": por.picture.size, "path": widget.picture(por.picture.path)}
        else:
            tmp["picture"] = {"id": por.picture_id, "name": "", "size": "", "path": ""}
        tmp["link"] = por.link
        if por.end_at:
            tmp["end_at"] = utils.local_datetime_to_str(por.end_at)
        else:
            tmp["end_at"] = ""
        tmp["skills"] = utils.loads(por.skills) if por.skills else []
        res.append(tmp)
    return {"error_code": 0, "msg": "ok", "portfolios": res}


def portfolio_add(user, params):
    name = params.get('name')
    detail = params.get('detail')
    picture_id = utils.safe_id(params.get('picture_id'))
    category_id = utils.safe_id(params.get('category_id'))
    link = params.get('link')
    end_at = params.get('end_at')
    if end_at:
        end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y-%m', utc=False)

    if not name or not detail or not category_id:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(name)) > 100 or link and len(link) > 100:
        return {"error_code": 20151, "msg": "name or address too long"}

    if picture_id:
        attachment = Attachment.select().where(Attachment.id == picture_id, Attachment.user == user).first()
        if not attachment:
            return {"error_code": 20153, "msg": "picture_id invalid"}

    portfolio = Portfolio()
    portfolio.user = user
    portfolio.name = name
    portfolio.detail = detail
    if picture_id:
        portfolio.picture = picture_id
    portfolio.category = category_id
    if link:
        portfolio.link = link
    if end_at:
        portfolio.end_at = end_at
    portfolio.save()

    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["portfolio",]})
    return {"error_code": 0, "msg": "ok", "portfolio_id": portfolio.id}


def portfolio_change(user, params):
    pid = utils.safe_id(params.get('pid'))
    name = params.get('name')
    detail = params.get('detail')
    picture_id = utils.safe_id(params.get('picture_id'))
    category_id = utils.safe_id(params.get('category_id'))
    link = params.get('link')
    end_at = params.get('end_at')
    if end_at:
        end_at = utils.str_to_datetime(params.get('end_at'), pattern='%Y-%m', utc=False)

    if not pid or not name or not detail or not category_id or not end_at:
        return {"error_code": 80002, "msg": "no enough parameters"}

    if len(unicode(name)) > 100 or len(link) > 100:
        return {"error_code": 20151, "msg": "name or address too long"}

    if not picture_id:
        picture_id = 0
    else:
        attachment = Attachment.select().where(Attachment.id == picture_id, Attachment.user == user).first()
        if not attachment:
            return {"error_code": 20153, "msg": "picture_id invalid"}

    portfolio = Portfolio.select().where(Portfolio.user == user, Portfolio.id == pid).first()
    if not portfolio:
        return {"error_code": 20152, "msg": "portfolio not exists"}

    portfolio.name = name
    portfolio.detail = detail
    portfolio.picture = picture_id
    portfolio.category = category_id
    portfolio.link = link
    portfolio.end_at = end_at if end_at else ""
    portfolio.update_at = utils.now()
    portfolio.save()

    return {"error_code": 0, "msg": "ok"}

def portfolio_remove(user, params):
    pid = utils.safe_id(params.get('pid'))
    if not pid:
        return {"error_code": 80002, "msg": "no enough parameters"}

    portfolio = Portfolio.delete().where(Portfolio.user == user, Portfolio.id == pid)
    if not portfolio:
        return {"error_code": 20152, "msg": "portfolio not exists"}

    portfolio.execute()
    queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["portfolio",]})
    return {"error_code": 0, "msg": "ok"}
