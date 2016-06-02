# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from models.address import Address
from common import utils
from peewee import SQL
from config.settings import cache


def address_list(params, lang):
    address_id = params.get("address_id", None)
    address_id = utils.safe_id(address_id)
    if type(address_id) == bool:
        return {"error_code": 80003, "msg": "parameters invalid"}
    t = params.get("t", None)
    if t == "all":
        cid = params.get("cid", None)
        cid = utils.safe_id(cid)
        if cid:
            addresses = cache.get("address_all_%s" % cid)
            if not addresses:
                Parent = Address.alias()
                GrandParent = Address.alias()
                addresses = (Address.select()
                             .join(Parent, on=(Address.parent == Parent.id))
                             .join(GrandParent, on=(Parent.parent == GrandParent.id))
                             .where(GrandParent.id == cid)
                             |
                             Address.select()
                             .join(Parent, on=(Address.parent == Parent.id))
                             .where(Parent.id == cid)
                             )
                addresses = addresses.order_by(SQL('id'))
                cache.put("address_all_%s" % cid, addresses)

        else:
            addresses = cache.get("address_all")
            if not addresses:
                addresses = Address.select().order_by(Address.id.asc())
                cache.put("address_all", addresses)

                for x in addresses:
                    cache.put("address_%s" % x.id, x)
    else:
        addresses = cache.get("address_p_%s" % address_id)
        if not addresses:
            addresses = Address.select().where(Address.parent == address_id)
            cache.put("address_p_%s" % address_id, addresses)

    out = []
    for a in addresses:
        out.append({"name": utils.lang_map_name(a.name, a.ename, lang), "address_id": a.id, "pid": a.parent_id})
    return {"error_code": 0, "msg": "ok", "addresses": out}

address_list({"t":"all", "address_id": 0}, "zh-CN")
