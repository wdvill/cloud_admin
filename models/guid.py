#-*- coding:utf-8 -*-

from .base import BaseModel

class GUID(BaseModel):
    @classmethod
    def guid(cls):
        c = cls.create()
        return c.id
