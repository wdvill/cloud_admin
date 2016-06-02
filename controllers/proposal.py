#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check
from backend import proposal


class ProposalBasic(Base):
    @signin_check
    def get(self):
        result = proposal.proposal_list_basic(self.user, self.params, self.lang)
        return self.send(result)

class Proposal(Base):
    @signin_check
    def get(self):
        result = proposal.proposal_list(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    def post(self):
        result = proposal.proposal_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = proposal.proposal_update(self.user, self.params)
        return self.send(result)

class ProposalMessage(Base):
    @signin_check
    def get(self):
        result = proposal.proposal_message_list(self.user, self.params)
        return self.send(result)

    @signin_check
    def post(self):
        result = proposal.send_message(self.user, self.params)
        return self.send(result)
