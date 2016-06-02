#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from models.question import Question
from config.settings import cache
from common import utils


def question_list(params, lang):
    qtype = params.get("qtype")
    if qtype not in ("user", "proposal_revoke_f", "proposal_refuse_c",
                     "proposal_refuse_f", "contract_refuse", "contract_revoke",
                     "proposal_archive", "contract_finish_c", "contract_finish_f"):
        return {"error_code": 20411, "msg": "qtype invalid"}

    question = cache.get("question_%s" % qtype)
    if not question:
        question = Question.select().where(Question.qtype == qtype).order_by(Question.level.desc())
        cache.put("question_%s" % qtype, question)

    out = [dict(
        question_id=q.id,
        name=utils.lang_map_name(q.name, q.ename, lang),
    ) for q in question]

    return {"error_code": 0, "msg": "ok", "questions": out}

