#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers import (
    page, user,
    system_user)

urls=[
    ("/", page.Index),
    ("/signin", system_user.Signin),
    ("/signout", system_user.Signout),
    ("/api/system_user", system_user.SystemUser),
    #("/api/user/signup", system_user.Register),
    ("/api/user/signin", system_user.Login),
    ("/api/user/signout", system_user.Logout),
    ("/api/user/password/reset", system_user.PasswordReset),
    ("/api/user/password/change", system_user.PasswordChange),
    ("/api/user/password/verify", system_user.PasswordVerify),


    ("/api/user/status", user.ChangeStatus),
    ("/api/user/list", user.UserList),
    
    ("/(.*)", page.NotFound)
]
