#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from config.settings import all_skills
from controllers.base import Base
from controllers.decorator import (api_check, signin_check, freelancer_check,
        public_setting_verify, client_check,)
from backend import contract
from backend import user
from backend import freelancer 
from common import queue


class JobsView(Base):
    @signin_check
    def get(self):
        return self.render("contract/freelancer-myjobs.html", first_nav="my_jobs", sec_nav="my_jobs")

class ContractDetailView(Base):
    @signin_check
    #@freelancer_check
    def get(self, uuid):
        return self.render("contract/show-contract.html", first_nav="my_jobs", sec_nav="contract")

class ContractsView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("contract/freelancer-list.html", first_nav="my_jobs", sec_nav="contract")

class DiaryView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("freelancer-daily.html", first_nav="my_jobs", sec_nav="diary")

class OfferDetailView(Base):
    @signin_check
    #@freelancer_check
    def get(self, uuid):
        sec_nav = "my_jobs" if self.user.identify[0] == "f" else "contract"
        return self.render("contract/offer.html", first_nav="my_jobs", sec_nav=sec_nav)

class StatsView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("freelancer/statistics.html", first_nav="find_job", sec_nav="stats")

class FreelancerSettings(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.redirect("/freelancers/settings/concatinfo")

class FreelancerSettingAccount(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("public-person-account.html", sider_nav="account")

class FreelancerSettingCards(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("public-wallet-bankcard.html", sider_nav="cards")

class FreelancerSettingAlipay(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("public-wallet-alipay.html", sider_nav="alipay")

class FreelancerSettingsInfo(Base):
    @signin_check
    @freelancer_check
    @public_setting_verify
    def get(self):
        return self.render("public-person-information.html", sider_nav="concatinfo")

class FreelancerSettingWithdrawal(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("account-withdrawal.html")

class FreelancerSettingRecharge(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("account-recharge.html")

class FreelancerSettingProfile(Base):
    @signin_check
    @freelancer_check
    @public_setting_verify
    def get(self):
        return self.render("public-setting-record.html", sider_nav="profile")

class FreelancerIdentity(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        profile = self.user.profile.first()
        if profile.id_number != "":
            return self.render("public-verify-identity-success.html", sider_nav="idverify")
        else:
            return self.render("public-verify-identity-nocheck.html", sider_nav="idverify")

class FreelancerSettingsPwd(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        return self.render("public-change-password.html", sider_nav="password")

class FreelancerSettingsQuestion(Base):
    @signin_check
    @public_setting_verify
    def get(self):
        qs = user.user_question(self.user)
        if qs["error_code"] == 0:
            return self.render("public-change-question.html",
                               user_questions=qs["questions"][0]["name"], sider_nav="question")
        return self.render("public-setting-question.html", sider_nav="question")

class FreelancerDetail(Base):
    @signin_check
    def get(self, uuid):
        skills = ",".join(all_skills)
        if self.user.uuid == uuid:
            return self.render("freelancer-detail.html", first_nav="find_job", sec_nav="data", skills=skills)
        else:
            return self.render("findjob-need-other-record.html", first_nav="find_job", sec_nav="data", skills=skills)

class FreelancerSettingTeam(Base):
    @signin_check
    #@freelancer_check
    #@public_setting_verify
    def get(self):
        return self.write("页面没出来")

class FreelancerFavorite(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("findjob-myfavorite.html", first_nav="find_job", sec_nav="favorite")

class FreelancerSubscribe(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("findjob-mysubscibe.html")

class FreelancerProposal(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("freelancer/proposal.html", first_nav="find_job", sec_nav="proposal")

class ReportView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        return self.render("report/report.html")

class FreelancerProposalDetail(Base):
    @signin_check
    @freelancer_check
    def get(self, proposal_id):
        return self.render("proposal/freelancer-detail.html", first_nav="find_job", sec_nav="proposal")

class CreateClientView(Base):
    @signin_check
    @freelancer_check
    def get(self):
        if self.user.to_req == True:
            return self.redirect("/freelancers/settings")
        return self.render("creat-client.html")

# 开发者报表
class FreelancerStats(Base):
    @signin_check
    @freelancer_check
    def get(self):
        result = freelancer.freelancer_report(self.user, self.params) 
        return self.send(result)

# 开发者统计
class FreelancerTongji(Base):
    @signin_check
    @freelancer_check
    def get(self):
        result = freelancer.freelancer_statis(self.user)
        return self.send(result)


class FreelancerContract(Base):
    @signin_check
    def get(self):
        result = contract.freelancer_contract(self.params)
        return self.send(result)
    

class ContractComplete(Base):
    @signin_check
    @freelancer_check
    def get(self, contract_id, milestone_id):
        return self.render("contract/check-submit-success.html", first_nav="my_jobs", sec_nav="contract")

class ContractDetail(Base):
    @signin_check
    @freelancer_check
    def get(self, contract_id, milestone_id):
        return self.render("contract/stone-detail.html", first_nav="my_jobs", sec_nav="contract")

class FreelancerRecommand(Base):
    @signin_check
    @client_check
    def get(self):
        result = freelancer.freelancer_recommend(self.user, self.params)
        return self.send(result)

class WeekStoneDiaryView(Base):
    @signin_check
    @freelancer_check
    def get(self, contract_id):
        return self.render("freelancer-daily.html")

class WeekStoneDiaryDetailView(Base):
    @signin_check
    def get(self, contract_id, shot_id):
        return self.render("dailylog-detail.html")

class DiscoverView(Base):
    @signin_check
    def get(self):
        uuid = self.params.get("user_id", "")
        if uuid:
            queue.to_queue({"type":"user_discover_view", "uuid":uuid, "user_id":self.user.id})
        return self.write({"error_code":0, "msg":"ok"})
