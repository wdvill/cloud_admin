#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import logging
import traceback

from backend import margin, proposal
from models.contract import Contract, MileStone, WeekStone, OrderBonus
from models.margin import Order
from common import utils, queue
from config.settings import database

logger = logging.getLogger(__name__)


def get_pay_order(user, params):
    """ 查询带支付订单 """
    contract_id = params.get("contract_id")
    trade_no = params.get("trade_no")
    ptype = params.get("ptype")
    if not contract_id or not trade_no or not ptype:
        return {"error_code": 20871, "msg": "params not enought"} 

    if ptype not in ("milestone", "weekstone", "bonus"):
        return {"error_code": 20872, "msg": "ptype invalid"} 
    
    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20873, "msg": "contract not exists"} 
    if contract.status not in ("unpaid", "paid", "carry", "pause"):
        return {"error_code": 20874, "msg": "contract status invalid"} 

    order = Order.select().where(Order.trade_no == trade_no).first()
    if not order:
        return {"error_code": 20875, "msg": "order not exists"} 
    if order.status != "process":
        return {"error_code": 20876, "msg": "order status invalid"} 

    amount = 0
    records = list()
    if ptype == "milestone":
        ms = MileStone.select().where(
            MileStone.order == order,
            MileStone.contract == contract,
            MileStone.status == "unpaid",
        )
        for m in ms:
            amount += m.amount
            records.append({
                "name": m.name,
                "amount": m.amount,
            }) 
        
    elif ptype == "weekstone":
        ws = WeekStone.select().where(
            WeekStone.order == order,
            WeekStone.contract == contract,
            WeekStone.status == "unpaid",
        ).first()
        amount = contract.amount
        records.append({
            "hourly": contract.hourly,
            "workload": contract.workload,
            "start_at": utils.local_datetime_to_str(ws.start_at),
        })
        
    elif ptype == "bonus":
        ob = OrderBonus.select().where(
            OrderBonus.order == order,
            OrderBonus.contract == contract,
            OrderBonus.status == "process",
        ).first()
        amount = ob.amount + ob.fee
        profile = ob.freelancer.profile.first()
        records.append({
            "amount": ob.amount,
            "fee": ob.fee,
            "description": ob.description,
            "freelancer": profile.name, 
        })
    cs = {"name": contract.name, "ptype": ptype, "contract_id": contract.uuid,
            "amount": utils.decimal_two(amount)
    }

    return {"error_code": 0, "msg": "ok", "contracts": cs, "records": records}


def order_payment(params):
    """ 支付订单 """
    contract_id = params.get("contract_id")
    trade_no = params.get("trade_no")
    ptype = params.get("ptype")
    if not contract_id or not trade_no or not ptype:
        return {"error_code": 20881, "msg": "params not enought"} 

    if ptype not in ("milestone", "weekstone", "bonus"):
        return {"error_code": 20882, "msg": "ptype invalid"} 
    
    order = Order.select().where(Order.trade_no == trade_no).first()
    if not order:
        return {"error_code": 20885, "msg": "order not exists"} 

    # 订单如果已经成功直接返回成功信息，为异步先于同步回调工作
    if order.status == "success":
        return {"error_code": 0, "msg": "ok", "contract_id": contract_id} 
    elif order.status == "fail":
        return {"error_code": 20886, "msg": "order status invalid"} 

    contract = Contract.select().where(Contract.uuid == contract_id).first()
    if not contract:
        return {"error_code": 20883, "msg": "contract not exists"} 

    if ptype != "bonus" and contract.status not in ("unpaid", "paid", "carry", "pause"):
        return {"error_code": 20884, "msg": "contract status invalid"}

    with database.atomic() as txn:
        try:
            # 里程碑支付
            if ptype == "milestone":
                qs = ((MileStone.order == order) & (MileStone.contract == contract) & (MileStone.status == "unpaid"))
                # 计算订单冻结金额
                ms = MileStone.select().where(qs)
                if not ms:
                    return {"error_code": 20887, "msg": "not found unpaid milestone"} 
                amount = 0
                for m in ms:
                    amount += m.amount

                client_margin = contract.team.user.margin.first()
                if client_margin.margin < amount:
                    return {"error_code": 20888, "msg": "client money not enought"}

                # 冻结
                pay_order = margin.freeze_amount(contract.team.user, contract.team, contract.job, amount, order)
                # 更新已经支付里程碑
                ms_update  = MileStone.update(status = "paid").where(qs)
                ms_update.execute()

                # 发送offer，更新合同状态
                if contract.status == "unpaid":
                    contract.status = "paid"
                    contract.save()
                    # 同步招标
                    proposal.client_send_offer(contract)
                    queue.to_queue({"type": "contract_new", "contract_id": contract.id})
                # 不是发送offer，自动开启下一个里程碑
                else:
                    ms = MileStone.select().where(MileStone.contract == contract, MileStone.status << ["carry", "carry_pay", "dispute"]).first()
                    if not ms:
                        ms = MileStone.select().where(MileStone.contract == contract, MileStone.status == "paid").order_by(MileStone.term.asc()).first()
                        ms.status = "carry"
                        ms.save()
                        contract.status = "carry"
                        contract.stone_status = "carry"
                        contract.save()
                return {"error_code": 0, "msg": "ok", "contract_id": contract.uuid, "job_id": contract.job.job_uuid}
            # 时薪支付
            elif ptype == "weekstone":
                ws = WeekStone.select().where(WeekStone.order == order, WeekStone.contract == contract, WeekStone.status == "unpaid").first()
                if not ws:
                    return {"error_code": 20889, "msg": "not found unpaid weekstone"} 

                client_margin = contract.team.user.margin.first()
                if client_margin.margin < contract.amount:
                    return {"error_code": 208810, "msg": "client money not enought"}

                pay_order = margin.freeze_amount(contract.team.user, contract.team, contract.job, contract.amount, order)
                ws.status = "paid"
                ws.save()
                # 发送offer，更新合同状态
                if contract.status == "unpaid":
                    contract.status = "paid"
                    contract.save()
                    # 同步招标
                    proposal.client_send_offer(contract)
                    queue.to_queue({"type": "contract_new", "contract_id": contract.id})
                # 不是发送offer，自动开启下一个里程碑
                else:
                    ws.status = "carry"
                    ws.save()
                    contract.status = "carry"
                    contract.stone_status = "carry"
                    contract.save()
                    queue.to_queue({"type": "weekstone_next_week", "weekstone_id": ws.id})
                return {"error_code": 0, "msg": "ok", "contract_id": contract.uuid, "job_id": contract.job.job_uuid}
            # 奖金支付
            elif ptype == "bonus":
                ob = OrderBonus.select().where(OrderBonus.order == order, OrderBonus.contract == contract, OrderBonus.status == "process").first()
                if not ob:
                    return {"error_code": 208811, "msg": "not found unpaid bonus"} 

                result = margin.transfer_pay(order_c=ob.order, order_f=ob.pay_order)
                ob.status = "success"
                ob.confirm_at = utils.now()
                ob.save()
                return {"error_code": 0, "msg": "ok", "contract_id": contract.uuid, "job_id": contract.job.job_uuid}
        except:
            logger.error(traceback.format_exc())
            txn.rollback()
            return {"error_code": 208812, "msg": "trade fail"}

