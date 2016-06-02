#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
   # linux
   log_path = "/tmp/"
elif _platform == "darwin":
   # MAC OS X
   log_path = "/tmp/"
elif _platform == "win32":
   # Windows
   log_path = "D:\\"

import logging
import logging.config

logging.config.dictConfig({
    'version': 1,              
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',

            'filename': log_path + "cloudwork-output.log",
            "encoding": "utf8",
            'formatter': 'standard'
        },
        'queue': {
            'level': 'INFO',
            'class': 'logging.FileHandler',

            'filename': log_path + "cloudwork-queue.log",
            "encoding": "utf8",
            'formatter': 'standard'
        },
        'idverify': {
            'level': 'INFO',
            'class': 'logging.FileHandler',

            'filename': log_path + "cloudwork-idverify.log",
            "encoding": "utf8",
            'formatter': 'standard'
        }
    },
    'loggers': {
        'controllers': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'models': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'backend': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'cron': {
            'handlers': ['console', 'queue'],
            'level': 'DEBUG',
        },
        'tasks': {
            'handlers': ['console', 'queue'],
            'level': 'DEBUG',
        },
        'idverify': {
            'handlers': ['console', 'idverify'],
            'level': 'DEBUG',
        }
    }
})
