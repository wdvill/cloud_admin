#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import help_center


class Help(Base):
    def get(self):
        res = help_center.topic(self.lang)
        if "keyword" in self.params:
            hot = help_center.help_search(self.params, self.lang)
            is_hot = False
        else:
            is_hot = True
            hot = help_center.hot(self.lang)
        return self.render("other/help-hot.html", topics=res["topics"], hots=hot["questions"], is_hot=is_hot)

class HelpDetail(Base):
    def get(self, uuid):
        res = help_center.topic(self.lang)
        detail = help_center.detail(self.lang, uuid)
        return self.render("other/help.html", topics=res["topics"], title=detail["title"], answer=detail['answer'])

class HelpTopic(Base):
    def get(self, tid):
        res = help_center.topic(self.lang)
        detail = help_center.topic_detail(tid, self.lang)
        return self.render("other/help-hot.html", topics=res["topics"], hots=detail["questions"], is_hot=False, tid=tid)
