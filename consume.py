#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import sys 
reload(sys)
sys.setdefaultencoding("utf8")

import time
import gevent
from gevent import monkey;monkey.patch_all()
from gevent.threadpool import ThreadPool
from config.settings import cron_queue, queue_conn, message_queue
from tasks import detect

#threadpool = ThreadPool(150)

def pull_msg():
    with queue_conn.connect():
        with queue_conn.SimpleQueue(cron_queue) as queue:
            for x in range(10):
                try:
                    message = queue.get(block=False, timeout=1)
                    detect.handle_msg(message)
                except queue.Empty:
                    break

        with queue_conn.SimpleQueue(message_queue) as queue:
            for x in range(10):
                try:
                    message = queue.get(block=False, timeout=1)
                    detect.handle_msg(message)
                except queue.Empty:
                    break

def main():
    #threadpool.join()
    while 1:
        #gevent.sleep(1)
        #threadpool.spawn(pull_msg)
        time.sleep(1)
        pull_msg()

if __name__ == "__main__":
    main()
