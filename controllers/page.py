#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import misc, job, banner, feedback, category
from config.settings import all_skills, all_languages, all_frameworks
from common import utils

class Index(Base):
    def get(self):
        if not self.user:
            return self.redirect("/signin")

        return self.render("index.html", categorys=category.get_index_category())

class Browse(Base):
    def get(self):
        #if self.user:
        #    if self.user.identify[0] == "f":
        #        return self.redirect("/find-work-home")
        #    else:
        #        return self.redirect("/clients/jobs")
        return self.render("browse-index.html")

class Legal(Base):
    def get(self):
        return self.render("legal/user-agreement.html")

class Privacy(Base):
    def get(self):
        return self.render("legal/privacy.html")

class AppVersion(Base):
    def post(self):
        result = misc.get_version(self.params, self.request)
        return self.send(result)

class Banner(Base):
    def get(self):
        result = banner.get_banners(self.params)
        return self.send(result)

class AllSkills(Base):
    def post(self):
        return self.send({"error_code":0, "msg":"ok", "skills":utils.dumps(all_skills)})

class About(Base):
    def get(self):
        return self.render("about/aboutus.html")

class Feedback(Base):
    def post(self):
        result = feedback.new_feedback(self.user, self.params)
        return self.send(result)

class Desktop(Base):
    def get(self):
        return self.render("appdown/app_down.html")

class ConcatUs(Base):
    def get(self):
        return self.render("about/contactus.html")

class JoinUs(Base):
    def get(self):
        return self.render("about/joinus.html")

class DesktopNetwork(Base):
    @signin_check
    def get(self):
        return self.send({"error_code":0})

class Download(Base):
    def get(self):
        return self.render("appdown/app_down.html")

class NotFound(Base):
    def get(self, u):
        return self.render("404.html")

class Messages(Base):
    @signin_check
    def get(self):
        return self.render("webim.html")
