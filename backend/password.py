#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from backend import pbkdf2
from common import utils

def generate_password(origin_password):
    salt = utils.rand_str()
    pw = pbkdf2.pbkdf2_hex(origin_password, salt, 10000)
    return pw, salt

def check_password(origin_password, encrypt_password, salt):
    return pbkdf2.pbkdf2_hex(origin_password, salt, 10000) == encrypt_password
