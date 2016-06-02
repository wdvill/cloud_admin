#!/usr/bine/vn python
# -*- coding:utf-8 -*-

from models.feedback import Feedback
from common import utils


def new_feedback(user, params):
    t = params.get("t", "suggest")
    if t not in ("bug", "suggest", "run_slow", "message_slow", "signin_slow", "unusual", "exit", "other"):
        return {"error_code":20721, "msg":"type invalid"}

    score = utils.safe_id(params.get("score", "0"))
    content = params.get("content", "")
    if not content or len(content) > 1024 * 20:
        return {"error_code":20722, "msg":"content must less than 20480"}
    if not score or not 0 <= score <= 10:
        score = 0

    contract = params.get("contract", "").strip()
    if contract and len(contract) > 50:
        return {"error_code":20723, "msg":"contract must less than 50"}

    fb = Feedback()
    fb.ftype = t
    fb.score = score
    fb.content = content
    fb.contract = contract
    if user:
        fb.user = user
        if user.identify[0] == "c":
            fb.team = user.identify[1:]
    fb.save()
    return {"error_code":0, "msg":"ok"}
