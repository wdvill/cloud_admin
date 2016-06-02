#!/usr/bine/vn python
# -*- coding:utf-8 -*-

from models.banner import Banner
from backend import widget

def get_banners(params):
    platform = params.get("platform", "app")
    if not platform:
        platform = "app"

    banners = Banner.select(Banner.title, Banner.image, Banner.link)\
                .where(Banner.platform==platform, Banner.visible==True).order_by(Banner.sortord.desc())

    out = []
    for x in banners:
        out.append({"title":x.title, "image":widget.picture(x.image), "link":x.link})
    return {"error_code":0, "msg":"ok", "banners":out}
