#!/usr/bin/env python
# -*- coding:utf-8 -*-

from config.settings import queue_conn, cron_queue, exchange, message_queue
import traceback
import logging
import utils

logger = logging.getLogger("tasks")


def to_queue(value):
    if not value or type(value) != dict or "type" not in value:
        return False

    try:
        with queue_conn.connect():
            with queue_conn.SimpleQueue(message_queue) as queue:
                value_str = utils.dumps(value)
                queue.put(value_str)
                #logger.error("enter queue: %s" % value_str)
    except:
        logger.error("%s" % traceback.format_exc())
    return True
