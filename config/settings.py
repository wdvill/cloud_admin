#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import os
import loadcf
import json
import argparse
from peewee import MySQLDatabase
from playhouse.shortcuts import RetryOperationalError
from jinja2 import FileSystemLoader, Environment
from kombu import Connection, Exchange, Queue
from config import log
from common import tpl_filter, cache as libcache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conf_name = ""

parser = argparse.ArgumentParser(description='Process config env')
parser.add_argument('-p', metavar='N', type=int, default=8080, 
                    help='an integer for the accumulator')
parser.add_argument('-c', help='select the config env. default: local', default="")
args = parser.parse_args()
conf_name = args.c
if conf_name:
    loadcf.load("%s/config/%s.json" % (BASE_DIR, conf_name))
else:
    try:
        loadcf.load("%s/config/local.json" % BASE_DIR)
    except:
        loadcf.load("%s/config/env.json" % BASE_DIR)

from loadcf import *

cookie_secret = ')#@a(750mv)cn&#@c#^y%52-pof*w%)ba%w5kd1*u0k=28&^$)'

class MyRetryDB(RetryOperationalError, MySQLDatabase):
    pass

database = MyRetryDB(mysql.db, host = mysql.host, user = mysql.user,
        passwd = mysql.passwd, charset = mysql.charset, port = mysql.port)

tpl_filter.TR_CN = json.loads(open(BASE_DIR + "/common/locale-zh-cn.json", "rb").read())
tpl_filter.TR_EN = json.loads(open(BASE_DIR + "/common/locale-en.json", "rb").read())

template = Environment(loader=FileSystemLoader('templates'), cache_size=-1, trim_blocks=True)
template.filters["timediff_format"] = tpl_filter.timediff_format
template.globals.update(_=tpl_filter.trans)
template.globals.update(_timediff=tpl_filter.trans_time)

# queue conf
exchange = Exchange(rabbitmq.exchange, "direct", durable=True)
cron_queue = Queue("cron", exchange=exchange, routing_key="cron")
message_queue = Queue("message", exchange=exchange, routing_key="message")
queue_conn = Connection("amqp://%s:%s@%s:%s/%s" % (rabbitmq.user, rabbitmq.password, rabbitmq.host, rabbitmq.port, rabbitmq.vhost))
# queue end

# cache
cache = libcache.Cache()

all_languages = ("Chinese", "Japanese", "Korean", "French", "Spanish")

pl = ("Java", "C", "C++", "C#", "Python", "PHP", "Javascript", "Ruby", "Perl",
        "Visual Basic .NET", "Delphi/Object Pascal", "Assembly language",
        "Visual Basic", "Objective-C", "Swift", "R", "Groovy", "MATLAB",
        "PL/SQL", "D", "Schema", "Dart", "Lisp", "Fortan", "Lua", "Scala",
        "Haskell", "Golang", "Erlang", "Rust", "Ada")

all_skills = ("Tomcat","Zeus","Lighttpd","IIS","Blackberry",
            "Symbian","Windows phone","Android","Linux",
            "Mac OS","Apache HTTP Server","Nginx","Mtk",
            "IOS ","Windows","Websphere Application Server",
            "Weblogic Server","Apusic Application Server",
            "Jetty","Resin","Geronimo","Jboss Application Server",
            "MS Access","BerkeleyDB","CouchDB","HANA","HBASE",
            "IBM DB2","Informix","Microsoft SQL Server","MongoDB",
            "MySQL","NoSQL","Oracle","CakePHP","PostgreSQL",
            "SQLite","Sybase","Teradata","Awt/Swing","C","C++",
            "C#","Eclipse","Eclipse PDE/RCP","Eclipse Plugin Development",
            "Eclipse SWT/JFace","J2SE","Java","COM/COM+","Delphi",
            "MFC","PowerBuilder","PowerScript","VBA","VC++",
            "Visual Studio","Winform","linux-app-development",
            "Qt","unix-systems-development","ActionScript",
            "Ajax","CSS/CSS3","DIV+CSS","flash","HTML/DHMTL",
            "JSON","ORM","Redis","RESTful","Silverlight","SOAP",
            "SoapUI","Bootstrap","XML","XQuery","XSLT/XPath",
            "Yii Framework","Zend Framework","symfony","smarty",
            "Silex Framework","Prado PHP Framework","PHPNuke",
            "PHPfox","Phing","moodle","lithium framework","kohana",
            "Joomla","fusebox","Drupal","CodeIgniter","Hibernate",
            "iBatis/MyBatis","Java EE"," Java Servlet","ICEfaces",
            "JBoss Seam","JSF ","JSP","Mockito","Apache Camel",
            "R1 BizFoundation","RMI"," Apache Cocoon","Spring Framework",
            "Apache CXF","Apache Tiles","AppFuse","SSH","struts",
            "backbone-js","dojo","ExtJS","limejs","mocha","mootools",
            "prototypejs","qooxdoo"," spine-dot-js","jQuery","Node.js",
            "JX","KISSY","QWrap","Tangram","Como","Sonic","Chart.js",
            "Zebra","Workless","Junior","Radi","HTML5 Bones",
            "Literally Canvas","Gauge.js","WYSIHTML5","HTML5 Sortable",
            "Lungo.JS","Kendo UI","Jo","52 Framework","G5 Framework",
            "django-framework","flask","Pylons","python-scipy",
            "Scrapy Framework","tastypie","zope","Oracle APEX",
            "perl-catalyst","perl-mojolicious","PerlDancer",
            "Play Framework","Ruby on Rails","Sinatra Framework",
            "Cocoa Touch","iOS-development","iPad","ipad-app-development",
            "iPhone","iphone-app-development"," Objective-C",
            "Quartz Composer","Xcode","Bluetooth","Brew","Cocos2d-x",
            "CoffeeScript","HBuilder","HTML5","J2ME","jQTouch",
            "jQueryMobile","PhoneGap"," Sencha Touch","TitaniumMobile",
            "Unity3D","WAP","ORMLite","ASP.NET",".NET Framework",
            "DevExpress","Entity Framework","IdeaBlade DevForce",
            "N2CMS","SharePoint","WCF","WPF","Photoshop","Firework",
            "Coreldraw","illustrator","Animation","Cartoon","Freehand",
            "3D Max","Autocad","Maya","Axure","Mockups","UI Design","PHP")

all_frameworks = ("Entity Framework",
                 "ADO.NET", "Adobe AIR",
                 ".NET Framework", "Core Java",
                 "Apple UIKit",
                 "JQuery", "Ext.js",
                 "Angular.js", "React.js", "Vue.js", "Spring Framework")

user_points_config = {
    "category": 5, "avatar": 8, "title": 5, "overview": 5, 
    "email": 5, "skills": 5, "english": 5, "other_language": 6,
    "workload": 5, "level": 5, "employment": 10, "education": 6, 
    "portfolio": 10, "hourly": 5, "location": 5, "address": 5,
    "postcode": 5
} 

