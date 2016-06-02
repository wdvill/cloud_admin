#-*- coding:utf-8 -*-

from common import utils
from models.misc import Misc

def get_version(params, request):
    ua = utils.resolve_agent(request.headers.get("User-Agent", ""))
    if not ua:
        return {"error_code":20061, "msg":"user-agent not exists"}

    app_type = {"a": "android_version", "i": "ios_version", "w": "winphone_version", "d":"desktop_version"}
    record = Misc.select().where(Misc.misc_key==app_type[ua['os']]).first()
    if not record:
        return {"error_code":20062, "msg":"upgrade error"}
    return {"error_code":0, "msg":"ok", "data": utils.loads(record.value)}


def misc_get_or_create(key, value=None, desc=""):
    misc = Misc.select().where(Misc.misc_key == key).first()
    if not misc:
        misc = Misc()
        misc.misc_key = key
        if value:
            if type(value) == dict:
                try:
                    misc.value = utils.dumps(value)
                except:
                    raise
            else:
                misc.value = value
        if desc:
            value.description = desc
        misc.save()
    return misc

def misc_get(key):
    misc = Misc.select().where(Misc.misc_key == key).first()
    return misc

def misc_create(key, value=None, desc=""):
    misc = Misc()
    misc.misc_key = key

    if type(value) == dict:
        misc.value = utils.dumps(value)
    else:
        misc.value = value
    misc.description = desc
    misc.save()
    return misc

def misc_update(key, value, misc=None, desc=""):
    if not misc:
        misc = Misc.select().where(Misc.misc_key == key).first()

    if not misc:
        return False

    if type(value) == dict:
        misc.value = utils.dumps(value)
    else:
        misc.value = value
    misc.description = desc
    misc.save()
    return True


def misc_delete(key):
    misc = Misc.delete().where(Misc.misc_key == key)
    if misc:
        misc.execute()
    return True


def generate_verify_init_data(user, mark):
    key = "{username}-{flag}-{mark}".format(username=user.username, flag="verify", mark=mark)
    value = dict(
        id_verify_count=0,
        last_verify_time=utils.now(),
    )
    return key, value
