#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base, EncryptBase
from controllers.decorator import signin_check, freelancer_check, client_check
from backend import user
from backend import system_user
from config.settings import all_skills, all_languages
from common import utils

class Create(Base):
    def post(self):
        device = "web"
        result = user.register(self.params, device)
        if result['error_code'] == 0:
            domain = utils.get_domain(self.request.host)
            self.set_cookie("session_token", result["session_token"], expires=result['expire_at'], path="/", domain=domain)
            self.set_cookie("cuid", result['identify'][0], expires=result['expire_at'], path="/")
        return self.send(result)
    
class UserList(Base):
    def get(self):
        user_list = user.user_list(self.params)
        return self.send( user_list)

class ChangeStatus(Base):
    """change user status"""
    def put(self):
        result = user.change_status(self.params)
        return self.send(result)
        pass

class SettingsRedirect(Base):
    @signin_check
    def get(self):
        if self.user.identify[0] == "f":
            return self.redirect("/freelancers/settings")
        return self.redirect("/clients/settings")
    
class PasswordReset(Base):
    def post(self):
        result = user.password_reset(self.params)
        return self.send(result)

class UserQuestion(Base):
    @signin_check
    def get(self):
        result = user.user_question(self.user)
        return self.send(result)

    @signin_check
    def post(self):
        result = user.question_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = user.question_update(self.user, self.params)
        return self.send(result)

class UserProfile(Base):
    @signin_check
    def get(self):
        # query_type:f means query freelancer, c means query client
        if self.is_desktop:
            self.user.identify = "f%s" % self.user.id

        if self.user.identify[0] == "f":
            query_type = "f"
        else:
            if self.params.get("uuid"):
                query_type = "f"
            else:
                query_type = "c"

        if query_type == "f":
            result = user.user_profile(self.user, self.params, self.lang)
        else:
            result = client.client_profile(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    def post(self):
        result = user.profile_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        if self.user.identify[0] == "f":
            result = user.user_profile_update(self.user, self.params)
        else:
            result = client.client_profile_update(self.user, self.params)
        return self.send(result)

