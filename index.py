#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import argparse
import os
import tornado
import tornado.wsgi
from config import settings, url


application = tornado.web.Application(handlers=url.urls, cookie_secret=settings.cookie_secret,
                                    debug=settings.debug, xsrf_cookies=False,
                                    static_path=os.path.join(os.path.abspath("."), "static"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process config env')
    parser.add_argument('-p', metavar='N', type=int, default=8080,
                        help='an integer for the accumulator')
    parser.add_argument('-c', help='select the config env. default: local')
    args = parser.parse_args()
    port = args.p

    application.listen(port)
    print("http://localhost:%s" % port)
    tornado.ioloop.IOLoop.instance().start()
