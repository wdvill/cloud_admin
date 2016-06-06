#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base, EncryptBase
from controllers.decorator import signin_check, freelancer_check, client_check
from backend import user, client
from backend import system_user
from config.settings import all_skills, all_languages
from common import utils

class Create(Base):
    def post(self):
        device = "web"
        result = user.register(self.params, device)
        if result['error_code'] == 0:
            domain = utils.get_domain(self.request.host)
            self.set_cookie("session_token", result["session_token"], expires=result['expire_at'], path="/", domain=domain)
            self.set_cookie("cuid", result['identify'][0], expires=result['expire_at'], path="/")
        return self.send(result)
    
class UserList(Base):
    def get(self):
        pass

class SettingsRedirect(Base):
    @signin_check
    def get(self):
        if self.user.identify[0] == "f":
            return self.redirect("/freelancers/settings")
        return self.redirect("/clients/settings")

class ChangeFreelancer(Base):
    @signin_check
    def get(self, uuid):
        result = user.change_role(self.user, uuid, "f")
        if result:
            self.set_cookie("cuid", "f", path="/", expires=utils.timedelta(utils.now(), days=7))
            return self.redirect("/find-work-home")
        return self.redirect("/")

class ChangeClient(Base):
    @signin_check
    def get(self, uuid):
        result = user.change_role(self.user, uuid, "c")
        if result:
            self.set_cookie("cuid", "c", path="/", expires=utils.timedelta(utils.now(), days=7))
            return self.redirect("/clients/jobs")
        return self.redirect("/")

class ForgotPassword(Base):
    def get(self):
        return self.render("forgotpassword.html")

class ForgotPasswordSuccess(Base):
    def get(self):
        return self.render("findpassword-success.html")

class PasswordReset(Base):
    def post(self):
        result = user.password_reset(self.params)
        return self.send(result)

class PasswordChange(Base):
    @signin_check
    def post(self):
        result = user.password_change(self.user, self.params)
        return self.send(result)

class PasswordVerify(Base):
    @signin_check
    def post(self):
        result = user.password_verify(self.user, self.params)
        return self.send(result)


# 注册完引导页
class Guide(Base):
    @signin_check
    def get(self):
        if self.user.status == "active":
            return self.redirect("/")
        st = self.user.reg_step
        #  本步骤完成后，页面停留到下一步
        if st == "category":
            return self.redirect("/users/profile/step/2")
        elif st == "profile":
            return self.redirect("/users/profile/step/3")
        elif st == "resume":
            return self.redirect("/users/profile/step/4")
        return self.render("profile-freelancer-guide.html")

# 注册第一步
class FreelancerCategoryCreate(Base):
    @signin_check
    @freelancer_check
    def get(self):
        if self.user.status == "active":
            return self.redirect("/")
        return self.render("select-category.html")

class FreelancerCategory(Base):
    @signin_check
    @freelancer_check
    def get(self):
        result = user.get_category(self.user, self.lang)
        return self.send(result)

    @signin_check
    @freelancer_check
    def post(self):
        result = user.category_create(self.user, self.params)
        return self.send(result)

    @signin_check
    @freelancer_check
    def put(self):
        result = user.category_update(self.user, self.params)
        return self.send(result)

# 注册第二步
class FreelancerProfileCreate(Base):
    @signin_check
    def get(self):
        # TODO 已完善过的用户不能进入
        if self.user.status == "active":
            return self.redirect("/")
        skills = ",".join(all_skills)
        return self.render("profile-create.html", skills=skills, languages=all_languages)


# 注册第三步
class FreelancerWorkAndEduCreateView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        # TODO 已完善过的用户不能进入
        if self.user.status == "active":
            return self.redirect("/")
        skills = ",".join(all_skills)
        return self.render("profile-freelancer-work-edu.html", skills=skills)

class FreelancerWorkAndEduCreate(Base):
    @signin_check
    @freelancer_check
    def post(self):
        result = user.profile_resume(self.user, self.params)
        return self.send(result)

# 注册第四步
class FreelancerOtherCreateView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        if self.user.status == "active":
            return self.redirect("/")
        return self.render("profile-other.html")

class FreelancerOtherCreate(Base):
    @signin_check
    @freelancer_check
    def post(self):
        result = user.other_create(self.user, self.params)
        return self.send(result)

# 注册完成
class FreelancerRegCompleteView(Base):
    @signin_check
    def get(self):
        if self.user.status == "active":
            return self.redirect("/")
        return self.render("profile-check.html", user=self.user)

class FreelancerRegComplete(Base):
    @signin_check
    def post(self):
        result = user.reg_complete(self.user, self.params)
        return self.send(result)

class UserQuestion(Base):
    @signin_check
    def get(self):
        result = user.user_question(self.user)
        return self.send(result)

    @signin_check
    def post(self):
        result = user.question_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        result = user.question_update(self.user, self.params)
        return self.send(result)

class UserProfile(Base):
    @signin_check
    def get(self):
        # query_type:f means query freelancer, c means query client
        if self.is_desktop:
            self.user.identify = "f%s" % self.user.id

        if self.user.identify[0] == "f":
            query_type = "f"
        else:
            if self.params.get("uuid"):
                query_type = "f"
            else:
                query_type = "c"

        if query_type == "f":
            result = user.user_profile(self.user, self.params, self.lang)
        else:
            result = client.client_profile(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    def post(self):
        result = user.profile_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def put(self):
        if self.user.identify[0] == "f":
            result = user.user_profile_update(self.user, self.params)
        else:
            result = client.client_profile_update(self.user, self.params)
        return self.send(result)


class CreateClient(Base):
    @signin_check
    @freelancer_check
    def post(self):
        result = user.create_client(self.user, self.params)
        return self.send(result)

    @signin_check
    def get(self):
        result = user.client_info(self.params, self.lang)
        return self.send(result)

class CreateFreelancer(Base):
    @signin_check
    @client_check
    def post(self):
        result = user.create_freelancer(self.user)
        return self.send(result)

class UserVerify(Base):
    @signin_check
    def post(self):
        result = user.identification(self.user, self.params)
        return self.send(result)


class UserRole(Base):
    @signin_check
    def get(self):
        result = user.user_role_list(self.user)
        return self.send(result)

    @signin_check
    def put(self):
        token = self.request.arguments.get("session_token", None)
        if not token:
            token = self.get_cookie("session_token")

        ua = self.request.headers.get("User-Agent", "")[:2]
        if ua == "a/":
            device = "android"
        elif ua == "i/":
            device = "ios"
        elif ua == "d/":
            device = "desktop"
        else:
            device = "web"

        result = user.user_role_change(self.user, self.params, token, device)
        return self.send(result)


class UserRoleChange(Base):
    @signin_check
    def get(self):
        result = user.user_role_change(self.user, self.params)
        return self.send(result)

class UserAlipay(Base):
    @signin_check
    def post(self):
        result = user.alipay_create(self.user, self.params)
        return self.send(result)

    @signin_check
    def delete(self):
        result = user.alipay_delete(self.user, self.params)
        return self.send(result)

class IMSessionVerify(EncryptBase):
    def get(self):
        result = user.im_session_verify(self.params)
        return self.send(result)

class GetJumpCode(Base):
    @signin_check
    def post(self):
        result = user.get_jump_code(self.user)
        return self.send(result)

class ClientJump(Base):
    def get(self):
        result = user.client_login(self.params)
        path = self.params.get("path")
        if result['error_code'] or not path or path[0] != "/":
            return self.redirect("/")

        domain = utils.get_domain(self.request.host)
        self.set_cookie("session_token", result["session_token"], expires=result['expire_at'], path="/", domain=domain)
        self.set_cookie("cuid", result['identify'][0], expires=result['expire_at'], path="/")

        return self.redirect(path)
