#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import logging

from controllers.base import Base, NoCSRFBase
from controllers.decorator import signin_check
from backend import margin

logger = logging.getLogger(__name__)


class BasicInfo(Base):
    @signin_check
    def get(self):
        result = margin.basic_info(self.user)
        return self.send(result)

class Record(Base):
    @signin_check
    def get(self):
        result = margin.record_list(self.user, self.params)
        return self.send(result)

class Bank(Base):
    @signin_check
    def get(self):
        result = margin.bank_list()
        return self.send(result)

class BankCard(Base):
    @signin_check
    def get(self):
        result = margin.card_list(self.user)
        return self.send(result)

    @signin_check
    def post(self):
        result = margin.bankcard_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = margin.bankcard_delete(self.user, self.params)
        return self.send(result)

class Deposit(Base):
    @signin_check
    def post(self):
        result = margin.deposit(self.user, self.params)
        return self.send(result)

class DepositCallback(Base):
    @signin_check
    def get(self):
        """ 支付宝页面跳转通知 """
        result = margin.deposit_result(self.user, self.params)
        extra = result["extra"]
        if result["error_code"] == 0:
            if extra.get("type") == "contract":
                url = "/clients/jobs/{0}#hire".format(result["job_id"])
                return self.redirect(url)
            return self.render("account-recharge-success.html", result=result)
        else:
            if extra.get("type") == "contract":
                url = "/clients/contracts/{0}/pay".format(extra["contract_id"])
                return self.redirect(url)
            return self.send(result)
    

class DepositCallbackSync(NoCSRFBase):
    def post(self):
        """ 支付宝异步毁掉通知 """
        result = margin.deposit_result_sync(self.user, self.params)
        return self.send(result)


class WithdrawAccounts(Base):
    @signin_check
    def get(self):
        result = margin.withdraw_accounts(self.user)
        return self.send(result)


class Withdraw(Base):
    @signin_check
    def post(self):
        result = margin.withdraw_freeze(self.user, self.params)
        return self.send(result)


