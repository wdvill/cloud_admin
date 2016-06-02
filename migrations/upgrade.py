#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


import os,sys
import glob
 
curdir = os.path.abspath("../")
sys.path.append(curdir)

from config.settings import database
from common import utils


def main():
    files = []
    for f in glob.glob("*.sql"):
        _,filename = os.path.split(f)
        files.append(filename)
    files.sort()

    try:
        database.execute_sql("CREATE TABLE `migration` ( `id` int(11) NOT NULL AUTO_INCREMENT, `action` varchar(255) NOT NULL DEFAULT '', `created_at` datetime DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8")
    except:
        pass

    for f in files:
        sql = "select id from migration where action='%s'" % f
        cursor = database.execute_sql(sql)
        rs = cursor.fetchall()
        if len(rs) == 0:
            execute(f)
    print("migration pass")

def execute(action):
    print("=" * 80)
    print("== migration %s" % action)
    print("=" * 80)
    with open(action, "rb") as fh:
        cont = fh.read()
        cont = cont.decode()
        lines = cont.split(";")
        lines = [x.strip() for x in lines if x.strip()!=""]

        for line in lines:
            if line and not line.startswith("--") and not line.startswith("/*"):
                print("execute sql : %s\n" % line)
                database.execute_sql(line)

        sql = "insert into migration (action, created_at) values ('%s','%s')" % (action, utils.now())
        database.execute_sql(sql)

if __name__ == "__main__":
    main()
