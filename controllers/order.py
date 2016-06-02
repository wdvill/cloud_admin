#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, client_check, freelancer_check
from backend import contract
from backend import order 

class OrderPayApi(Base):
    @signin_check
    @client_check
    def get(self):
        result = order.get_pay_order(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = order.order_payment(self.params)
        return self.send(result)

class OrderPayView(Base):
    @signin_check
    @client_check
    def get(self, uuid, ptype, trade_no):
        if ptype == "bonus":
            return self.render("bonus-pay.html")
        else:
            return self.render("contract-pay.html", sec_nav="my_jobs")


