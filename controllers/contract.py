#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, client_check, freelancer_check
from backend import contract


class ContractBasic(Base):
    @signin_check
    def get(self):
        result = contract.contract_list_basic(self.user, self.params)
        return self.send(result)

class Contract(Base):
    @signin_check
    def get(self):
        if self.is_desktop:
            self.user.identify = "f%s" % self.user.id
        result = contract.contract_list(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = contract.contract_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = contract.contract_operate(self.user, self.params)
        return self.send(result)

class MileStone(Base):
    @signin_check
    def get(self):
        result = contract.milestone_list(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = contract.milestone_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = contract.milestone_audit(self.user, self.params)
        return self.send(result)

class MileStonePay(Base):
    @signin_check
    def get(self):
        result = contract.milestone_pay_get(self.user, self.params)
        return self.send(result)

class WeekStone(Base):
    @signin_check
    def get(self):
        result = contract.weekstone_list(self.user, self.params)
        return self.send(result)

class WeekStonePay(Base):
    @signin_check
    @client_check
    def get(self):
        result = contract.weekstone_pay_get(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = contract.weekstone_create(self.user, self.params)
        return self.send(result)
    
    @signin_check
    @client_check
    def put(self):
        result = contract.weekstone_audit(self.user, self.params)
        return self.send(result)


class WeekStoneTime(Base):
    @signin_check
    def get(self):
        result = contract.get_weekstone_time(self.user, self.params)
        return self.send(result)

# 截屏
class WeekStoneShot(Base):
    @signin_check
    def get(self):
        if self.is_desktop:
            self.user.identify = "f%s" % self.user.id
        result = contract.shot_list(self.user, self.params)
        return self.send(result)

    @signin_check
    def post(self):
        result = contract.shot_create(self.user, self.params)
        return self.send(result)

    @signin_check
    @freelancer_check
    def put(self):
        result = contract.shot_update(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = contract.shot_delete(self.user, self.params)
        return self.send(result)


class ContractFreelancers(Base):
    @signin_check
    def get(self):
        result = contract.contract_freelancers(self.user, self.params)
        return self.send(result)


# 合同支付页面
class ContractPay(Base):
    @signin_check
    @client_check
    def get(self, contract_id):
        return self.render("contract-pay.html") 

class Evaluate(Base):
    @signin_check
    def post(self):
        result = contract.contract_evaluate(self.user, self.params)
        return self.send(result)

class DesktopWeekStone(Base):
    @signin_check
    def get(self):
        result = contract.get_desktop_weekstone(self.user, self.params)
        return self.send(result)

class ContractWeekStoneList(Base):
    @signin_check
    def get(self):
        result = contract.contract_weekstone_list(self.user, self.params)
        return self.send(result)


class ContractSendBonus(Base):
    @signin_check
    @client_check
    def get(self):
        result = contract.contract_bonus_query(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = contract.contract_bonus_order(self.user, self.params)
        return self.send(result)

class TestContractWeekStoneAudit(Base):
    @signin_check
    def get(self):
        result = contract.test_contract_weekstone_audit(self.params)
        return self.send(result)
