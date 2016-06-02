#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import sys 
reload(sys)
sys.setdefaultencoding("utf8")

import time
from config.settings import cron_queue, queue_conn
import logging
from common import utils
import schedule

logger = logging.getLogger("cron")

# 检查offer是否过期
def check_offer_expire():
    logger.error("%s check expire offer" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "check_offer_expire"})

# 汇总按小时工作日志, 每天统计前一周的
def count_weekstone():
    logger.error("%s count weekstone" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "count_weekstone"})

# 按小时工作，未操作，自动打款
def auto_pay_weekstone():
    logger.error("%s auto pay weekstone" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "auto_pay_weekstone"})

# 每天生成按小时工作报表
def generate_weekstone_day_report():
    logger.error("%s generate weekstone day report" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "weekstone_day_report"})

# 统计90天内查看数
def calc_user_discover():
    logger.error("%s calc freelancer discover" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "calc_user_discover"})

# 清除session
def cleanup_session():
    logger.error("%s cleanup session" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type": "cleanup_session"})

# 测试
def test():
    logger.error("%s generate test queue" % utils.now())
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            queue.put({"type":"create_group", "group_name":"测试团队",
                            "user_id_list":[120, 104], "group_type":1,
                            "user_id":144, "team_id":104,
                            "req_user_id":120, "proposal_id":3, "contract_id":1})

def main():
    #schedule.every(0.1).minutes.do(test)

    schedule.every(10).minutes.do(check_offer_expire)
    schedule.every(60).minutes.do(cleanup_session)
    # 每天统计工作日志
    schedule.every().day.at("00:01").do(count_weekstone)
    # 每天检查是否超过两天没有审核
    schedule.every().day.at("00:03").do(auto_pay_weekstone)
    schedule.every().day.at("00:01").do(generate_weekstone_day_report)
    schedule.every().day.at("00:10").do(calc_user_discover)

    while 1:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
