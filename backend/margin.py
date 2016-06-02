#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import decimal
import logging
import traceback

from .alipaybase import AlipayBase
from models.margin import Margin, MarginRecord, Order, Bank, Card, PayInfo
from models.contract import MarginContractRecord, Contract, OrderBonus
from models.team import Team
from common import utils, queue
from config.settings import database, alipay_config, host
from backend import sms
from peewee import fn


logger = logging.getLogger(__name__)


def basic_info(user):
    margin = user.margin.first()
    if not margin:
        margin = Margin()
        margin.user = user
        margin.save()

    if user.identify[0] == "f":
        return {"error_code":0, "msg":"ok", "margin":margin.margin,
                "withdraw":margin.withdraw, "income":margin.income}

    team_margin = Team.select().where(Team.id==int(user.identify[1:])).first()
    return {"error_code":0, "msg":"ok", "margin":margin.margin,
            "withdraw":margin.withdraw, "trust_amount":team_margin.trust_amount,
            "expend_amount":team_margin.expend_amount}

def bank_list():
    banks = Bank.select()
    out = []
    for x in banks:
        out.append({"id":x.id, "name":x.name, "code":x.code})
    return {"error_code":0, "msg":"ok", "banks":out, "logo_uri":"%s/static/images/bank/" % host}

def record_list(user, params):
    start_at = utils.str_to_date(params.get("start_at"), utc=False)
    end_at = utils.str_to_date(params.get("end_at"), utc=False)
    rtype = params.get("rtype", "all") 
    report = params.get("report", "false")
    pagenum = params.get("pagenum", "1")
    pagesize = params.get("pagesize", "10")

    if not pagenum or not pagesize or not str(pagenum).isdigit() or not str(pagesize).isdigit():
        return {"error_code":20191, "msg":"params invalid"}
    
    if rtype not in ("pay", "freeze", "refund", "income", "bonus", "all"):
        return {"error_code":20193, "msg":"rtype invalid"}

    if report == "true" and user.identify[0] != "f" and (not start_at or not end_at):
        return {"error_code":20194, "msg":"start_at or end_at invalid"}

    pagenum = int(pagenum)
    pagesize = int(pagesize)

    if not 5 <= pagesize <= 100:
        return {"error_code":20192, "msg":"pagesize invalid"}

    qs, qs_client = None, None
    if user.identify[0] == "f":
        qs = ((MarginRecord.user == user) & (MarginRecord.team == 0))
    else:
        qs = (MarginRecord.team == int(user.identify[1:]))

    # 只查询成功记录
    qs = (qs & (Order.status == "success"))

    # 报表查询
    if report == "true":
        if user.identify[0] == "f":
            qs = (qs & (MarginRecord.record_type << ["income", "bonus"]))
        else:
            # 需求者报表查询有开始时间和截止时间
            start_at = utils.datetime_day_min(start_at)
            end_at = utils.datetime_day_max(end_at)
            qs = (qs & (Order.confirm_at.between(start_at, end_at)))
            # 需求者报表统计三种分类金额
            qs_client = (qs & (MarginRecord.record_type << ["freeze", "pay", "refund"]))
    
    # 根据类型查询
    if rtype != "all":
        qs = (qs & (MarginRecord.record_type == rtype))

    records = MarginRecord.select(MarginRecord).join(Order).where(qs)
    count = records.count()
    records = records.order_by(MarginRecord.create_at.desc()).paginate(pagenum, pagesize)
    out = []
    for x in records:
        if x.margin > x.currently:
            t = "D"
        else:
            t = "W"

        job_detail = dict()
        if x.order.job_id:
            job = x.order.job
            job_detail["name"] = job.name 
            job_detail["team_name"] = job.team.name
        
        out.append({
            "trade_no": x.order.trade_no,
            "create_at": utils.local_datetime_to_str(x.create_at),
            "description": x.description, "amount":x.amount, "margin": x.margin,
            "type": t, "record_type": x.record_type, "job": job_detail,
            "fee": x.order.fee,
        })

    result = {"error_code":0, "msg":"ok", "records":out, "count": count, "pagenum": pagenum}
    
    # 为需求方报表统计额外数据
    if report == "true":
        if user.identify[0] == "f":
            income = MarginRecord.select(fn.sum(MarginRecord.amount)).join(Order).where(qs).scalar()
            result["income"] = income
        else:
            user_margin = user.margin.first()
            result["margin"] = utils.decimal_two(user_margin.margin)

            # 统计
            mr = MarginRecord.select(
                MarginRecord.record_type, fn.sum(MarginRecord.amount)
            ).join(Order).where(qs_client).group_by(MarginRecord.record_type).tuples()
            result.update({"refund": 0, "freeze": 0, "pay": 0})
            for key, value in mr:
                result[key] = value

    return result

def card_list(user):
    cards = Card.select(Card, Bank).join(Bank).where(Card.user == user)
    out = []
    for x in cards:
        out.append({"card_id":x.id, "card_no":x.card_no, "bank":x.bank.name, "bank_code":x.bank.code})
    return {"error_code":0, "msg":"ok", "cards":out, "logo_uri":"%s/static/images/bank/" % host}


def bankcard_create(user, params):
    card_no = params.get("card_no", "")
    code = params.get("code", "")
    if not card_no or not code:
        return {"error_code":20201, "msg":"parameter invalid"}
    bank = Bank.select().where(Bank.code == code).first()
    if not bank:
        return {"error_code":20202, "msg":"bank not exists"}
    if len(card_no) < 15 or not card_no.isdigit():
        return {"error_code":20203, "msg":"card number invalid"}
    card = Card.select().where(Card.user == user, Card.card_no == card_no).first()
    if card:
        return {"error_code":20204, "msg":"card is exist"}
    card = Card()
    card.bank = bank
    card.user = user
    card.card_no = card_no
    card.save()
    return {"error_code":0, "msg":"ok", "card_id": card.id}

def bankcard_delete(user, params):
    card_id = params.get("card_id", "")
    if not card_id:
        return {"error_code":20211, "msg":"card number invalid"}
    card = Card.select().where(Card.id == card_id, Card.user == user).first()
    if not card:
        return {"error_code":20212, "msg":"card is not exist"}
    card.delete_instance()
    return {"error_code":0, "msg":"ok"}

def deposit(user, params):
    amount = params.get("amount", "")
    amount = utils.decimal_two(amount)
    if amount is None:
        return {"error_code": 204410, "msg":"amount invalid"}

    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.amount = amount
    order.status = "process"
    order.order_type = "deposit"
    order.confirm_at = utils.now()
    order.save()

    margin = user.margin.first()
    mr = MarginRecord()
    mr.user = user
    if user.identify[0] != "f":
        mr.team = user.identify[1:]
    mr.amount = order.amount
    mr.record_type = "deposit"
    mr.currently = margin.margin
    mr.margin = margin.margin + order.amount
    mr.order = order
    mr.save()

    # 充值逻辑，生成url, payinfo表
    payinfo = PayInfo()
    payinfo.user = user
    payinfo.order = order
    profile = user.profile.first()
    payinfo.alipay = profile.alipay 
    payinfo.save()
    
    ap = AlipayBase()
    # add extra params for alipay
    extra = dict()
    dtype = params.get("dtype")
    if dtype in ("contract", "bonus"):
        contract_id = params.get("contract_id")
        contract = Contract.select().where(Contract.uuid == contract_id).first()
        if not contract_id or not contract:
            return {"error_code": 20449, "msg": "contract_id invalid"}
        
        extra["contract_id"] = contract_id
        extra["trade_no"] = trade_no 
        if dtype == "bonus":
            trade_no = params.get("trade_no")
            bonus = OrderBonus.select(OrderBonus).join(Order, on=(OrderBonus.order == Order.id)).where(Order.trade_no == trade_no).first() 
            if not trade_no or not bonus or bonus.status != "process":
                return {"error_code": 204411, "msg": "trade_no invalid"}

            extra["ptype"] = "bonus" 
        else:
            if contract.hourly == 0:
                extra["ptype"] = "milestone" 
            else:
                extra["ptype"] = "weekstone" 

    else:
        extra["type"] = "margin"

    data = {
        "out_trade_no": trade_no,
        "subject": u"充值",
        "total_fee": amount,
        "return_url": alipay_config["return_url"],
        "notify_url": alipay_config["notify_url"],
        "extra_common_param": utils.dumps(extra),
    }
    try:
        url = ap.create_direct_pay_by_user_url(**data)
        return {"error_code": 0, "msg": "ok", "url": url, "data":data}
    except:
        return {"error_code": 20441, "msg": "deposit fail"}


def deposit_result_sync(user, params):
    """ 异步通知接口 """
    trade_type = params.get("notify_type")
    if not trade_type or trade_type != "trade_status_sync":
        return {"error_code": 20521, "msg": "alipay params invalid"}

    result = _deposit_callback(user, params)
    if result["error_code"] == 0:
        extra = result["extra"]
        if extra.get("ptype") in ("milestone", "weekstone"):
            result = _deposit_contract_margin(extra)
        return "success"
    return result 
    

def deposit_result(user, params):
    """ 充值同步调整 """
    result = _deposit_callback(user, params)
    if result["error_code"] == 0:
        extra = result["extra"]
        if extra.get("ptype") in ("milestone", "weekstone"):
            result = _deposit_contract_margin(extra)
    return result
    

def _deposit_contract_margin(extra):
    """ 回调处理合同充值 """
    from backend.order import order_payment
    result = order_payment(extra)
    result["extra"] = extra
    return result


def _deposit_callback(user, params):
    trade_no = params.get("out_trade_no", "")
    trade_status = params.get("trade_status")
    amount = params.get("total_fee")
    seller_email = params.get("seller_email")
    extra= params.get("extra_common_param")
    extra= utils.loads(extra) if extra else ""

    if not trade_no or not trade_status or not amount or seller_email != alipay_config["seller"]:
        return {"error_code": 20446, "msg": "alipay params invalid", "extra": extra}

    order = Order.select().where(Order.trade_no == trade_no).first()
    if not order:
        return {"error_code": 20443, "msg": "order not exists", "extra": extra}

    margin = order.user.margin.first()
    # 如果异步先返回结果，同步则返回成功 
    if order.status == "success":
        return {"error_code": 0, "msg": "ok", "trade_no": trade_no, "amount": amount, "balance": margin.margin, "extra": extra}
    elif order.status == "fail":
        return {"error_code": 20444, "msg": "order already finish", "trade_no": trade_no, "amount": amount, "balance": margin.margin, "extra": extra}


    ap = AlipayBase()
    try:
        if not ap.verify_notify(**params):
            return {"error_code": 20442, "msg": "alipay invalid", "extra": extra}
    except Exception, e:
        logger.error(traceback.print_exc())
        return {"error_code": 20442, "msg": "alipay invalid", "extra": extra}

    if order.amount != utils.decimal_two(amount):
        return {"error_code": 20445, "msg": "amount does not equal", "extra": extra}

    with database.atomic() as txn:
        try:
            if trade_status not in ("TRADE_FINISHED", "TRADE_SUCCESS"):
                order.status = "fail"
                order.confirm_at = utils.now()
                order.save()
                return {"error_code": 20448, "msg": "recharge fail", "extra": extra}
            else:
                order.status = "success"
                order.confirm_at = utils.now()
                order.save()

                margin.margin += order.amount
                margin.update_at = utils.now()
                margin.save()
                # send msg to user
                mrecord = order.mrecord.first()
                queue.to_queue({"type": "margin_deposit_success", "mrecord_id": mrecord.id})
                return {"error_code": 0, "msg": "ok", "trade_no": trade_no, "amount": amount, "balance": margin.margin, "extra": extra}
        except Exception, e:
            logger.error(traceback.print_exc())
            txn.rollback()
            return {"error_code": 20447, "msg": "deposit fail", "extra": extra}

# 退款
def refund_amount(user, team, job, amount):
    margin = user.margin.first()
    if margin.freeze < amount:
        raise Exception, "freeze has no enoug money, freeze %s amount %s" % (margin.freeze, amount)

    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.amount = amount
    order.job = job
    order.status = "success"
    order.order_type = "refund"
    order.confirm_at = utils.now()
    order.save()

    mr = MarginRecord()
    mr.user = user
    mr.amount = amount
    mr.team = team
    mr.record_type = "refund"
    mr.currently = margin.margin
    mr.margin = margin.margin + amount
    mr.order = order
    mr.save()

    team.trust_amount -= amount
    if team.trust_amount < 0:
        team.trust_amount = 0
    team.save()

    margin.margin += amount
    margin.freeze -= amount
    if margin.freeze < 0:
        raise Exception, "freeze error: margin %s freeze %s" % (margin.margin, margin.freeze)

    margin.update_at = utils.now()
    margin.save()
    return order


# 生成一份进行中的订单
def process_order(user, team, job, amount):
    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.job = job
    order.amount = amount
    order.status = "process"
    order.save()
    return order


# 冻结金额, 托管
# 合同充值后支付请必须传入已经存在的订单
def freeze_amount(user, team, job, amount, order=None):
    margin = user.margin.first()
    if margin.margin < amount:
        raise Exception, "margin has no enoug money, margin %s amount %s" % (margin.margin, amount)

    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    if order and order.status != "process":
        raise Exception, "order status already closed. order_id: %s, order_status: %s"% (order.id, order.status)

    if not order:
        order = Order()
        order.user = user
        order.trade_no = trade_no
        order.job = job
        order.amount = amount
    order.status = "success"
    order.order_type = "freeze"
    order.confirm_at = utils.now()
    order.save()

    mr = MarginRecord()
    mr.user = user
    mr.team = team
    mr.amount = amount
    mr.record_type = "freeze"
    mr.currently = margin.margin
    mr.margin = margin.margin - amount
    mr.order = order
    mr.save()

    team.trust_amount += amount
    team.save()

    margin.margin -= amount
    if margin.margin < 0:
        raise Exception, "margin has no enoug money, margin %s amount %s" % (margin.margin, amount)
    margin.freeze += amount
    margin.update_at = utils.now()
    margin.save()
    return order

# 转账需求者订单
def transfer_order(user, team, freelancer, amount, order_type="bonus"):
    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    margin_c = user.margin.first()
    
    # 将金额格式化成两位小数在计算 
    amount = utils.decimal_two(amount)
    fee = utils.decimal_two(amount * decimal.Decimal(0.1))
    amount -= fee

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.fee = fee
    order.amount = amount
    order.status = "process"
    order.order_type = order_type 
    order.save()

    mr = MarginRecord()
    mr.user = user
    mr.amount = amount
    mr.team = team
    mr.record_type = order_type
    mr.currently = margin_c.margin
    mr.margin = margin_c.margin - fee - amount
    mr.order = order
    mr.save()

    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    margin_f = freelancer.margin.first()

    order_f = Order()
    order_f.user = freelancer 
    order_f.trade_no = trade_no
    order_f.amount = amount
    order_f.status = "process"
    order_f.order_type = order_type
    order_f.save()
    
    mr_f = MarginRecord()
    mr_f.user = freelancer 
    mr_f.amount = amount
    mr_f.record_type = order_type
    mr_f.currently = margin_f.margin
    mr_f.margin = margin_f.margin + amount
    mr_f.order = order
    mr_f.save()
    return order, order_f 


def transfer_pay(order_c, order_f):
    if order_c.status != "process" or order_f.status != "process":
        raise Exception, "order status invalid" 
    
    now = utils.now()
    margin_c = order_c.user.margin.first() 
    
    pay_money = order_c.amount + order_c.fee
    if margin_c.margin < pay_money:
        raise Exception, "client money not enought"

    # 需求者减钱
    margin_c.margin -= pay_money 
    margin_c.update_at = now  
    margin_c.save()
    # 开发者加钱
    margin_f = order_f.user.margin.first()
    margin_f.margin += order_f.amount 
    margin_f.update_at = now
    margin_f.save()
    # 更新交易记录 
    order_c.status = "success"
    order_c.confirm_at = now 
    order_c.save()

    order_f.status = "success"
    order_f.confirm_at = now
    order_f.save()
    # 消费金额 
    queue_amount = str(utils.decimal_two(order_c.amount + order_c.fee))
    mrecord = order_c.mrecord.first()
    queue.to_queue({"type": "statistics_team_amount", "team_id": mrecord.team_id, "amount": queue_amount})
    return True

# 付款给开发者
def payment_freelancer(user, freelancer, team, amount, job):
    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    client_margin = user.margin.first()
    if client_margin.freeze < amount:
        raise Exception, "freeze has no enoug money, freeze %s amount %s" % (client_margin.freeze, amount)

    amount = utils.decimal_two(amount)
    fee = amount * decimal.Decimal(0.1)
    amount -= fee

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.fee = fee
    order.amount = amount
    order.status = "success"
    order.job = job
    order.order_type = "pay"
    order.confirm_at = utils.now()
    order.save()

    mr = MarginRecord()
    mr.user = user
    mr.amount = amount
    mr.team = team
    mr.record_type = "pay"
    mr.currently = client_margin.margin
    mr.margin = client_margin.margin
    mr.order = order
    mr.save()

    client_margin.freeze -= amount
    client_margin.update_at = utils.now()
    client_margin.save()
    # 消费金额
    queue_amount = str(utils.decimal_two(order.amount + order.fee))
    queue.to_queue({"type": "statistics_team_amount", "team_id": team.id, "amount": queue_amount})

    # 需求者增加累计支付,减少托管金额
    team.expend_amount += amount
    team.trust_amount -= amount
    if team.trust_amount < 0:
        team.trust_amount = 0
    team.save()

    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    f_margin = freelancer.margin.first()

    f_order = Order()
    f_order.user = freelancer
    f_order.trade_no = trade_no
    f_order.amount = amount
    f_order.status = "success"
    f_order.job = job
    f_order.order_type = "income"
    f_order.confirm_at = utils.now()
    f_order.save()

    f_mr = MarginRecord()
    f_mr.user = freelancer
    f_mr.amount = amount
    f_mr.record_type = "income"
    f_mr.currently = f_margin.margin
    f_mr.margin = f_margin.margin + amount
    f_mr.order = order
    f_mr.save()

    f_margin.margin += amount
    # 增加累计收入
    f_margin.income += amount

    f_margin.update_at = utils.now()
    f_margin.save()
    return order

# 提现
def withdraw_amount(user, amount, team=None):
    margin = user.margin.first()
    if margin.margin < amount:
        raise Exception, "withdraw: margin has no enoug money, margin %s amount %s" % (margin.margin, amount)

    today = utils.datetime_to_number(utils.now())[2:]
    trade_no = "%s%s" % (today, utils.rand_num())
    while Order.select(Order.id).where(Order.trade_no==trade_no).first():
        trade_no = "%s%s" % (today, utils.rand_num())

    order = Order()
    order.user = user
    order.trade_no = trade_no
    order.amount = amount
    order.status = "process"
    order.order_type = "withdraw"
    order.confirm_at = utils.now()
    order.save()

    mr = MarginRecord()
    mr.user = user
    if team:
        mr.team = team
    mr.amount = amount
    mr.record_type = "withdraw"
    mr.currently = margin.margin
    mr.margin = margin.margin - amount
    mr.order = order
    mr.save()

    margin.margin -= amount
    if margin.margin < 0:
        raise Exception, "withdraw: margin has no enoug money, margin %s amount %s" % (margin.margin, amount)
    margin.freeze += amount
    margin.withdraw += amount
    margin.update_at = utils.now()
    margin.save()
    return order


# 登记合同交易记录
def margin_contract_record(contract, order, milestone=None, weekstone=None):
    margin_record = order.mrecord.first()
    
    mcr = MarginContractRecord()
    mcr.margin_record = margin_record 
    mcr.contract = contract
    if milestone:
        mcr.milestone = milestone
    if weekstone:
        mcr.weekstone = weekstone
    mcr.save()
    return mcr


def withdraw_accounts(user):
    out = []
    profile = user.profile.first()
    if profile.alipay:
        out.append({"card_no": profile.alipay, "bank": "alipay"})
    cards = Card.select(Card, Bank).join(Bank).where(Card.user == user)
    for x in cards:
        out.append({"card_no":x.card_no, "bank":x.bank.name})

    return {"error_code": 0, "msg": "ok", "accounts": out}

# 申请提现
def withdraw_freeze(user, params):
    amount = params.get("amount")
    amount = utils.decimal_two(amount)
    account = params.get("account") 
    account_type = params.get("type")
    phone_code = params.get("code")
    
    if not amount or not account or not account_type or not phone_code:
        return {"error_code": 20534, "msg": "params not enought"}

    sms_status = sms.verify_code(user.phone, phone_code)
    if sms_status["error_code"] != 0:
        return sms_status

    with database.atomic() as txn:
        try:
            team = user.identify[1:] if user.identify[0] != "f" else None
            order = withdraw_amount(user=user, team=team, amount=amount)
            
            payinfo = PayInfo()
            payinfo.user = user
            payinfo.order = order
            if account_type == "alipay":
                payinfo.alipay = account
            else:
                payinfo.card_no = account
            payinfo.save()

            margin = user.margin.first()
            # send message to user
            mrecord = order.mrecord.first()
            queue.to_queue({"type": "margin_withdraw_apply", "mrecord_id": mrecord.id})
            return {"error_code": 0, "msg": "ok", "amount": amount, "baclance": utils.decimal_two(margin.margin)}
        except Exception, e:
            txn.rollback()
            logger.error(traceback.print_exc())
            return {"error_code": 20533, "msg": e.message}

