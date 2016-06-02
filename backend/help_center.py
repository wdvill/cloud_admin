#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from models.help import Topic, Question
from common import utils
from config.settings import cache



def topic(lang):
    ts = Topic.select(Topic.name, Topic.id)
    topic = []
    for x in ts:
        topic.append({"name":x.name, "id":x.id})
    return {"error_code":0, "msg":"ok", "topics":topic}

def hot(lang):
    hot = []
    qs = Question.select().where(Question.hotspot==True)
    for y in qs:
        hot.append({"title":y.title, "id":y.uuid})
    return {"error_code":0, "msg":"ok", "questions":hot}

def topic_detail(tid, lang):
    out = []
    qs = Question.select().where(Question.topic==tid)
    for y in qs:
        out.append({"title":y.title, "id":y.uuid})
    return {"error_code":0, "msg":"ok", "questions":out}


def detail(lang, uuid):
    qs = Question.select().where(Question.uuid==uuid).first()
    if not qs:
        return {"error_code":1, "msg":"not exist"}

    return {"error_code":0, "msg":"ok", "title":qs.title, "answer":qs.answer}

# 帮助搜索
def help_search(params, lang):
    keyword = params.get("keyword", "")
    out = []
    if not keyword:
        return {"error_code":0, "msg":"ok", "questions":out}

    qs = Question.select().where(Question.title.contains(keyword) | Question.answer.contains(keyword))
    for y in qs:
        out.append({"title":y.title, "id":y.uuid})
    return {"error_code":0, "msg":"ok", "questions":out}
