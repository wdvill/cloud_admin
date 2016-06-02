#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from controllers.base import Base
from controllers.decorator import api_check, signin_check, template_check, freelancer_check , client_check
from config.settings import all_skills, all_languages, all_frameworks, pl
from backend import job


class JobNew(Base):
    @signin_check
    @client_check
    def get(self):
        skills = ",".join(all_skills)
        languages = ",".join(pl)
        frameworks = ",".join(all_frameworks)
        return self.render("project.html", skills=skills,
                           languages=languages, frameworks=frameworks, first_nav="my_jobs", sec_nav="job_new")

class JobEditView(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        skills = ",".join(all_skills)
        languages = ",".join(pl)
        frameworks = ",".join(all_frameworks)
        return self.render("project.html", skills=skills,
                           languages=languages, frameworks=frameworks,sec_nav="job_new")

class JobFind(Base):
    @signin_check
    def get(self):
        return self.render("index-findjob.html", first_nav="find_job", sec_nav="find_job")

class IndexJobFind(Base):
    def get(self):
        return self.render("index-findjob.html")

class JobSearch(Base):
    def post(self):
        result = job.search(self.user, self.params)
        return self.send(result)

class JobHome(Base):
    @signin_check
    @freelancer_check
    def get(self):
        if self.user.status != "active":
            return self.redirect("/users/guide")
        return self.render("findjob-mysubscibe.html", first_nav="find_job", sec_nav="find_job")

class JobSet(Base):
    @signin_check
    def get(self):
        result = job.get_job_list(self.user, self.params, self.lang)
        return self.send(result)

    @signin_check
    @client_check
    def post(self):
        result = job.new_job(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def put(self):
        result = job.edit_job(self.user, self.params)
        return self.send(result)

    @signin_check
    @client_check
    def delete(self):
        result = job.delete_job(self.user, self.params)
        return self.send(result)

class JobStatus(Base):
    @signin_check
    @client_check
    def put(self):
        result = job.job_status_update(self.user, self.params)
        return self.send(result)

class MyJobList(Base):
    @signin_check
    @client_check
    def get(self):
        result = job.get_my_jobs(self.user, self.params)
        return self.send(result)

class JobDetail(Base):
    @signin_check
    def get(self, uuid):
        return self.render("project-detail.html", first_nav="find_job", sec_nav="find_job")

class JobNewComplete(Base):
    @signin_check
    @client_check
    def get(self, uuid):
        result = job.get_job(uuid, self.user)
        if result['error_code']:
            # TODO 404
            pass
        return self.render("client/need-release-success.html", job=result["job"])

class JobFreelancerProposal(Base):
    @signin_check
    @freelancer_check 
    def get(self, uuid):
        result = job.get_job(uuid, self.user)
        return self.render("developer-bid.html", job=result['job'])

class JobProposal(Base):
    @signin_check
    @client_check
    def get(self):
        result = job.job_proposal(self.user, self.params, self.lang)
        return self.send(result)

class FreelancerRecommand(Base):
    @signin_check
    @client_check
    def get(self):
        result = job.job_freelancer_recommand(self.user, self.params, self.lang)
        return self.send(result)
