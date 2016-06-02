#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import friend


class FriendList(Base):
    @signin_check
    def get(self):
        res = friend.friend_list(self.user, self.is_mobile)
        return self.send(res)

class FriendUsersList(Base):
    @signin_check
    def get(self):
        res = friend.get_users_info(self.params)
        return self.send(res)
