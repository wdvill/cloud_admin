#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Cache(dict):
    def get(self, key):
        try:
            return self[key]
        except:
            return None

    def put(self, key, value):
        self[key] = value

    def delete(self, key):
        try:
            del self[key]
        except:
            pass

    def __repr__(self):
        return '<Cache by zhenjing ' + dict.__repr__(self) + '>'
