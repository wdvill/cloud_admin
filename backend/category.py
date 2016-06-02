#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from models.category import Category, CategoryOptions
from common import utils
from config.settings import cache


def category_list(params, lang="zh_CN"):
    category_id = utils.safe_id(params.get("category_id"))
    if type(category_id) == bool:
        return {"error_code":80003, "msg":"parameters invalid"}
    t = params.get("t", None)
    if t == "all":
        cates = cache.get("category_all")
        if not cates:
            cates = Category.select().order_by(Category.id.asc())
            cache.put("category_all", cates)
            for x in cates:
                cache.put("category_%s" % x.id, x)
    else:
        key = "category_p_%s" % category_id
        cates = cache.get(key)
        if not cates:
            cates = Category.select().where(Category.parent==category_id)
            cache.put(key, cates)

    out = []
    for c in cates:
        out.append({"name": utils.lang_map_name(c.name, c.ename, lang), "category_id": c.id, "pid": c.parent_id})
    return {"error_code": 0, "msg": "ok", "categorys": out}

def get_index_category():
    out = cache.get("category_index")
    if not out:
        cates = Category.select().order_by(Category.id.asc())

        out = {}
        for x in cates:
            if x.parent_id == 0:
                out[x.id] = {"id":x.id, "name":x.name, "children":[]}

        for m in cates:
            if m.parent_id != 0:
                out[m.parent_id]["children"].append({"id":m.id, "name":m.name, "pid":m.parent_id})
        cache.put("category_index", out)
    return out


def get_category_option(params):
    category_id = params.get("category_id", "4")

    op = CategoryOptions.select().where(CategoryOptions.category == category_id).first()
    out = {}
    if op:
        out.update({"stage":op.stage, "language":op.language, "api":op.api, 
                    "framework":op.framework, "platform":op.platform})
    return {"error_code":0, "msg":"ok", "options":out}

category_list({"t": "all", "category_id": 0})
