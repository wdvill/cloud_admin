#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import time
import mimetypes
import hashlib
from qiniu import Auth, put_data, BucketManager
from config.settings import qiniu_key


class Storage:
    def __init__(self):
        self.storage = Auth(qiniu_key.ak, qiniu_key.sk)
        self.bucket = BucketManager(self.storage)

    def generate_path(self, filename, t):
        id_ = str(uuid.uuid4())
        return '{type}-{uuid}-{ts}{ext}'.format(
            type = t,
            uuid = id_,
            ts = int(time.time()),
            ext = os.path.splitext(filename.rstrip())[1].lower(),
        )

    def mime_type(self, filename):
        return mimetypes.guess_type(filename)[0] or "application/octet-stream"

    def upload(self, filename, data, ftype="job"):
        path = self.generate_path(filename, ftype)
        token = self.storage.upload_token(qiniu_key.bucket, path)
        ret, info = put_data(token, path, data, mime_type=self.mime_type(filename), check_crc=True)
        md5 = hashlib.md5(data).hexdigest()
        size = len(data)
        if ret and info.status_code == 200:
            return {"path": path, "md5": md5, "size": size}
        return None

    def download(self, path):
        return "%s/%s" % (qiniu_key.uri, path)
