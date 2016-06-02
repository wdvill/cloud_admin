cloudwork
=================

The yunzujia 2.0

Create virtualenv
-----------------
    $ virtualenv env

Install python packages
-----------------
    $ source env/bin/activate
    $ pip install -r requirements.txt

Create database
-----------------
create database on UTF8 
    
    mysql> CREATE DATABASE cloudwork DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

create database user
    
    mysql> INSERT INTO mysql.user(Host,User,Password) values("localhost","yzj",password("yunzujia"));

add Permissions

    mysql> grant all privileges on cloudwork.* to yzj@localhost identified by 'yunzujia';

flush system permissions 
    
    mysql>flush privileges;

Run
----------

  source  env/bin/activate
  python index.py

  test env: python index.py -c test

  new port: python index.py -p 8081

Deploy
----------
    source  env/bin/activate
    pip install fabric

    webpack
    $> fab -f deploy.py deploy_test --set webpack=true
    no webpack
    $> fab -f deploy.py deploy_test


Migration
-----------------
    $ source env/bin/activate
    $ cd migrations
    $ python upgrade.py


Languages or skills required
----------------------------
Programming language: `Python2.7`, `Javascript`
Database: `mysql`
Backend Template: `jinja2`
FrontEnd: `Vue.js`


Documentation
--------------

peewee: [http://peewee.readthedocs.org](http://peewee.readthedocs.org)

jinja2: [http://jinja.pocoo.org](http://jinja.pocoo.org)

vue.js: [http://cn.vuejs.org](http://cn.vuejs.org)


Promise
-----------

  `html`, `css`, `js` tab is 2 space


Frontend
-----------

1、Install[node环境](https://nodejs.org/)，node版本>4.0,建议4.4.0

2、Install bower: `npm install -g bower`

3、Install bower packages:`bower install`

4、Install webpack: `cd rabbit & npm install`

API Reference
-------------
[API](https://github.com/yunzujia/cloudwork/blob/master/API.md)


