#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement
import cStringIO
from PIL import Image
from backend.qiniu_storage import Storage
from models.attachment import Attachment
from common import utils, queue
from config.settings import qiniu_key


def upload(user, params, upload_file):
    t = params.get("t", "")
    if t == "avatar":
        return upload_avatar(user, params, upload_file)

    if t == "logo":
        if user.identify[0] == "f":
            return {"error_code": 20044, "msg": "freelancer not allow upload logo"}
        return upload_avatar(user, params, upload_file, "logo")

    if t not in ("job", "contract", "milestone", "proposal", "portfolio", "contract", "milestone", "shot", "company", "article"):
        return {"error_code":20043, "msg":"type error"}

    if t == "shot" and not _detect_filetype(upload_file):
        return {"error_code":20044, "msg":"must be image"}

    if len(upload_file['filename']) > 200:
        return {"error_code":20041, "msg":"filename is less than 200 char"}
    storage = Storage()
    res = storage.upload(upload_file['filename'], upload_file['body'], t)
    if not res:
        return {"error_code":20042, "msg":"upload error"}
    attach = Attachment()
    attach.name = upload_file['filename']
    attach.path = res['path']
    attach.size = res['size']
    attach.md5 = res['md5']
    attach.atype = t
    attach.user = user
    attach.save()
    return {"error_code":0, "msg":"ok", "attachment_id": attach.id,
            "name": attach.name, "path": qiniu_key.uri + "/" + attach.path,
            "md5": attach.md5, "size": attach.size,
            "file_path": qiniu_key.uri + "/" + attach.path}

def _detect_filetype(upload_file):
    typedata = upload_file['body'][:10].encode('hex')
    ftype = ''
    if typedata.startswith('ffd8'):
        ftype = '.jpg'
    elif typedata.startswith('424d'):
        ftype = '.bmp'
    elif typedata.startswith('474946'):
        ftype = '.gif'
    elif typedata.startswith('89504e470d0a1a0a'):
        ftype = '.png'
    else:
        ftype = None
    return ftype

def upload_avatar(user, params, upload_file, utype="avatar"):
    x = params.get("x", "")
    y = params.get("y", "")
    w = params.get("w", "")
    h = params.get("h", "")
    boundx = params.get("boundx", "")
    boundy = params.get("boundy", "")

    if not x or not y or not w or not h or not boundx or not boundy \
            or not x.isdigit() or not y.isdigit() or not w.isdigit() or not h.isdigit() or not boundx.isdigit() or not boundy.isdigit():
        return {"error_code":20171, "msg":"avatar parameters invalid"}
    if len(upload_file) > 1024 * 1024 * 5:
        return {"error_code":20172, "msg":"avatar size less than 5M"}

    ftype = _detect_filetype(upload_file)
    if ftype is None:
        return {"error_code":20173, "msg":"avatar type error"}

    # 头像默认320
    size = 320
    params['x'], params['y'], params['w'], params['h'] = int(x), int(y), int(w), int(h)
    params['boundx'], params['boundy'] = int(boundx), int(boundy)
    s = cStringIO.StringIO(upload_file['body'])
    image = Image.open(s)

    w,h = image.size

    if params and params['boundx'] > 0:
        #web client
        if w > h:
            ratio = float(w) / params['boundx']
        else:
            ratio = float(h) / params['boundy']
        #print(ratio)
        params['w'] = int(round(ratio * params['w']))
        params['h'] = int(round(ratio * params['h']))
        params['x'] = int(round(ratio * params['x']))
        params['y'] = int(round(ratio * params['y']))
        image = image.crop((params['x'],params['y'],params['x']+params['w'],params['y']+params['h']))
        w,h = image.size

    if w == h:
        im_ss = image.resize((size,size))
    elif w < h:
        if w >= size:
            im_ss = image.crop((0,0,size,size))
        else:
            im_ss = image.crop((0,0,w,w))
            im_ss = im_ss.resize((size,size))
    else:
        if h >= size:
            im_ss = image.crop((0,0,size,size))
        else:
            im_ss = image.crop((0,0,h,h))
            im_ss = im_ss.resize((size,size))
    
    ss = cStringIO.StringIO()
    if im_ss.mode != "RGB":
        im_ss = im_ss.convert("RGB")
    im_ss.save(ss, "JPEG")
    content = ss.getvalue()

    storage = Storage()
    res = storage.upload(upload_file['filename'], content, ftype="avatar")
    if not res:
        return {"error_code":20174, "msg":"upload error"}

    if utype == "avatar":
        profile = user.profile.first()
        profile.avatar = res['path']
        profile.save()
        queue.to_queue({"type": "user_completeness", "user_id": user.id, "columns": ["avatar",]})
    else:
        # team logo
        team = user.team.first()
        team.logo = res['path']
        team.save()

    attach = Attachment()
    attach.name = upload_file['filename']
    attach.path = res['path']
    attach.size = res['size']
    attach.md5 = res['md5']
    attach.atype = "avatar"
    attach.user = user
    attach.save()
    
    return {"error_code":0, "msg":"ok", "avatar":qiniu_key.uri + "/" + res['path']}

def download(params):
    storage = Storage()
    attach = Attachment.select().where(Attachment.md5==params['path']).first()
    if not attach:
        return {"error_code":20051, "msg":"attachment not exists"}
    download_url = storage.download(attach.path)
    return {"error_code":0, "msg":"ok", "download_url": download_url}
