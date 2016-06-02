#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, public_setting_verify
from backend import notify 


class Notify(Base):
    @signin_check
    def get(self):
        result = notify.notify_list(self.user, self.params) 
        return self.send(result)

    @signin_check
    def put(self):
        result = notify.notify_read(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = notify.notify_delete(self.user, self.params)
        return self.send(result)


class NotifyView(Base):
    @signin_check
    def get(self):
        return self.render("notify.html")
    
class NotifySettings(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("client/client-setting-notify.html", sider_nav="notify")
    
class NotifyUserSetting(Base):
    @signin_check
    def get(self):
        result = notify.notify_setting_list(self.user)
        return self.send(result)

    @signin_check
    def post(self):
        result = notify.notify_setting_update(self.user, self.params)
        return self.send(result)
