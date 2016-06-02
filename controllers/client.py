#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import signin_check, client_check, public_setting_verify
from backend import contract, client, user, job
from common import queue

class GuideView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("employment-process.html")

class JobsView(Base):
    @signin_check
    @client_check
    def get(self):
        res = client.has_publish_check(self.user)
        if not res:
            return self.redirect("/clients/guide")

        return self.render("myproject.html", first_nav="my_jobs", sec_nav="my_jobs")

class OfferNewView(Base):
    @signin_check
    @client_check
    def get(self, proposal_id):
        return self.render("client/contract-create.html", first_nav="my_jobs", sec_nav="contract")

class OfferNewDirectView(Base):
    @signin_check
    @client_check
    def get(self, jod_uuid, user_id):
        return self.render("client/contract-direct.html",sec_nav="contract")

class ProposalView(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        result = job.get_job(uuid, self.user)
        queue.to_queue({"type":"job_proposal_view", "uuid":uuid, "user_id":self.user.id})
        return self.render("applicant-list.html",sec_nav="my_jobs", job=result["job"])

class Settings(Base):
    @signin_check
    @client_check
    @public_setting_verify
    def get(self):
        return self.render("client/client-setting-info.html", sider_nav="concatinfo")

class IndentifySettings(Base):
    @signin_check
    @client_check
    @public_setting_verify
    def get(self):
        profile = self.user.profile.first()
        if profile.id_number != "":
            return self.render("public-verify-identity-success.html", sider_nav="idverify")
        else:
            return self.render("client/client-setting-identify.html", sider_nav="idverify")

class ConIndentifySettings(Base):
    @signin_check
    @client_check
    @public_setting_verify
    def get(self):
        return self.render("client/client-setting-conidentify.html", sider_nav="companyverify")

class CreateFreelancerView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/client-setting-newfreelancer.html")
        
class ContractPayView(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        # 分为按小时和固定
        res = contract.get_contract_job(uuid)
        if res == 'hour':
            return self.render("client/client-journal.html", first_nav="freelancer", sec_nav="diary")
        elif res == 'fixed':
            return self.render("release-capital.html")
        else:
            return self.render("contract-pay.html", sec_nav="my_jobs")

class ContractPayActive(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        # 分为按小时和固定
        res = contract.get_contract_job(uuid)
        if res == 'hour':
            return self.render("release-capital-active.html")
        elif res == 'fixed':
            return self.render("release-capital-active.html")
        else:
            return self.render("404")

class StatsView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.redirect("/clients/reports/weekly")
        #return self.render("release-capital.html", first_nav="reports")

class ContractsView(Base):
    @signin_check
    @client_check
    def get(self):
        res = client.has_publish_check(self.user)
        if not res:
            return self.redirect("/clients/guide")

        return self.render("contract-list.html", first_nav="my_jobs", sec_nav="contract")

class FreelancerFindView(Base):
    @signin_check
    def get(self):
        return self.render("findperson-list.html", first_nav="freelancer", sec_nav="find")

# 首页搜索
class IndexFreelancerFindView(Base):
    def get(self):
        return self.render("findperson-list.html")

class FreelancerInviteView(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        u = user.get_user_by_uuid(uuid)
        if u:
            return self.render("client/send-invite.html", first_nav="my_jobs", sec_nav="", freelancer=u)

        return self.render("404")

class FreelancerSearch(Base):
    def get(self):
        result = client.search_freelancer(self.user, self.params, self.lang)
        return self.send(result)

class FreelancerView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.redirect("/clients/freelancers/waiting")
        #return self.render("employment-service.html", first_nav="freelancer", sec_nav="freelancer")

class FreelancerSavedView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("freelancer/employment-service.html", first_nav="freelancer", sec_nav="freelancer")

class FreelancerHiredView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("freelancer/employ_list.html", first_nav="freelancer", sec_nav="freelancer")

class FreelancerWaitView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("freelancer/sign_contract_list.html", first_nav="freelancer", sec_nav="freelancer")

class StatsWeeklyView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/weekly.html", first_nav="reports", sec_nav="weekly")

class StatsTimeSheetView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/timesheet.html", first_nav="reports", sec_nav="timesheet")

class StatsBudgetView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/budget.html", first_nav="reports", sec_nav="budget")

class DiaryView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/client-diary.html", first_nav="freelancer", sec_nav="diary")

class StatsTradeView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/trade.html", first_nav="reports", sec_nav="trade")

class ClientVerify(Base):
    @signin_check
    @client_check
    def post(self):
        result = client.client_verify(self.user, self.params)
        return self.send(result)

class FreelancerList(Base):
    @signin_check
    @client_check
    def get(self):
        result = client.get_client_freelancers(self.user)
        return self.send(result)


# 每周总结
class WeeklySummary(Base):
    @signin_check
    @client_check
    def get(self):
        result = client.week_summary_report(self.user, self.params)
        return self.send(result)


# 预算, 查所有的合同
class StatsBudget(Base):
    @signin_check
    @client_check
    def get(self):
        result = client.budget_report(self.user, self.params)
        return self.send(result)


# 工时，统计
class TimeSheet(Base):
    @signin_check
    @client_check
    def get(self):
        result = client.timesheet_report(self.user, self.params)
        return self.send(result)


# 结束合同评价1
class ContractEvaluate(Base):
    @signin_check
    #@client_check
    def get(self, contract_id):
        return self.render("contract/finish-contract.html")


# 结束合同评价2
class ContractFeedback(Base):
    @signin_check
    #@client_check
    def get(self, contract_id):
        return self.render("contract/finish-contract2.html")


# 需求者查看所有项目列表
class JobsListView(Base):
    @signin_check
    @client_check
    def get(self):
        return self.render("client/alljobs.html", first_nav="my_jobs", sec_nav="my_jobs")

class WeekStoneDiaryView(Base):
    @signin_check
    @client_check
    def get(self, contract_id):
        return self.write("需求者查看工作日志页")

class ContractAddMilestone(Base):
    @signin_check
    @client_check
    def get(self, contract_id):
        return self.render("contract/add-milestone.html")

