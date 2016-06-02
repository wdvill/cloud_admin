#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement
import datetime
import traceback
import ujson as json
import logging
from . import contract, message, statistics
from backend import notify

logger = logging.getLogger(__name__)

#def msg_ack(func):
#    def wrapper(params):
#        func(params)
#        params.ack()
#    return wrapper

mapping = {"check_offer_expire": contract.check_offer_expire,
            "count_weekstone": contract.count_weekstone,
            "auto_pay_weekstone": contract.auto_pay_weekstone,
            "create_group": message.create_group,
            "weekstone_day_report": contract.weekstone_day_report,
            
            "contract_start": [notify.contract_start, statistics.contract_start],
            "contract_freelancer_finish": [notify.contract_freelancer_finish, statistics.contract_finish],
            "contract_client_finish": [notify.contract_client_finish, statistics.contract_finish],
            "proposal_client_refuse": notify.proposal_client_refuse,
            "proposal_freelancer_refuse": notify.proposal_freelancer_refuse,
            "proposal_freelancer_accept": [notify.proposal_freelancer_accept, ],
            "proposal_client_accept": [notify.proposal_client_accept, statistics.increase_proposal_ok],
            "proposal_freelancer_active": [notify.proposal_freelancer_active, statistics.increase_proposal],
            "proposal_freelancer_reactive": notify.proposal_freelancer_reactive,
            "user_discover_view":statistics.user_discover_view,
            "user_discover":statistics.user_discover,
            "user_password_change": notify.user_password_change,
            "user_question_create": notify.user_question_create,
            "user_register": notify.user_register,
            "margin_withdraw_apply": notify.margin_withdraw_apply,
            "margin_deposit_success": notify.margin_deposit_success,
            "contract_expire": notify.contract_expire,
            "contract_refuse": notify.contract_refuse,
            "contract_new": notify.contract_new,
            "client_identify_apply": notify.client_identify_apply,
            "job_new": [notify.job_new, statistics.statistics_team_jobs],
            "user_identify": notify.user_identify,
            "milestone_client_unpass": notify.milestone_client_unpass,
            "milestone_client_pass": notify.milestone_client_pass,
            "milestone_freelancer_audit": notify.milestone_freelancer_audit,
            "milestone_create": notify.milestone_create,
            "contract_client_pause": notify.contract_client_pause,
            "contract_client_restart": notify.contract_client_restart,
            "proposal_client_active": [notify.proposal_client_active, ],
            "contract_revoke": notify.contract_revoke,
            "job_status_change": [notify.job_status_change, statistics.statistics_team_jobs],

            "contract_evaluate": [statistics.evaluate, notify.contract_evaluate, ],
            "statistics_team_amount": statistics.statistics_team_amount,

            "calc_user_discover":statistics.calc_user_discover,
            "cleanup_session": statistics.cleanup_session,

            "user_completeness": statistics.user_completeness,
            "job_proposal_view": statistics.job_view,
            "weekstone_shot_first": notify.weekstone_shot_first,
            "weekstone_freelancer_audit": notify.weekstone_freelancer_audit,
            "freelancer_shot_first": notify.freelancer_shot_first,
            "contract_dispute_start": notify.contract_dispute_start,
            "weekstone_client_pass": notify.weekstone_client_pass,
            "weekstone_next_week": notify.weekstone_next_week,

            }

def handle_msg(msg):
    logger.error("msg body: %s" % msg.body)
    body = json.loads(msg.body)

    start = datetime.datetime.now()
    logger.error("%s start: %s" % (body["type"], start))

    if body['type'] in mapping:
        try:
            func = mapping[body['type']]
            if type(func) == list:
                for fn in func:
                    fn(body)
            else:
                func(body)
            end = datetime.datetime.now() - start
            logger.error("%s end: %s, cost: %sS" % (body["type"], datetime.datetime.now(), end.total_seconds()))
        except:
            logger.error(traceback.format_exc())
            return
    else:
        logger.error("type %s cannot mapping" % body['type'])
    msg.ack()
