#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from peewee import CharField, IntegerField, ForeignKeyField, DateTimeField, DecimalField, FloatField
from .base import BaseModel
from .user import User
from .team import Team
from common import utils

class TeamStatistics(BaseModel):
    user = ForeignKeyField(User)
    team = ForeignKeyField(Team)
    eveluate_num = IntegerField(verbose_name="评价数量", null=False, default=0)
    total_amount = DecimalField(verbose_name="消费总金额", null=False, max_digits=10, decimal_places=2, default=0)
    score = IntegerField(verbose_name="评价总分", null=False, default=0)
    aver_score = FloatField(verbose_name="平均评分", null=False, default=0)
    hours = IntegerField(verbose_name="总雇佣时长", null=False, default=0)
    jobs = IntegerField(verbose_name="总发布工作", null=False, default=0)
    hires = IntegerField(verbose_name="总招聘人数", null=False, default=0)
    open_jobs = IntegerField(verbose_name="公开工作数", null=False, default=0)

    class Meta:
        db_table = "team_statistics"

class UserStatistics(BaseModel):
    user = ForeignKeyField(User, related_name="stats")
    eveluate_num = IntegerField(verbose_name="评价数量", null=False, default=0)
    score = IntegerField(verbose_name="评价总分", null=False, default=0)
    aver_score = FloatField(verbose_name="平均评分", null=False, default=0)
    total_amount = DecimalField(verbose_name="收入总金额", null=False, max_digits=10, decimal_places=2, default=0)
    hours = IntegerField(verbose_name="工作总时长", null=False, default=0)
    proposal = IntegerField(verbose_name="投标总数", null=False, default=0)
    success = IntegerField(verbose_name="投标成功次数", null=False, default=0)
    recommend = IntegerField(verbose_name="被推荐次数", null=False, default=0)
    coop = IntegerField(verbose_name="合作次数", null=False, default=0)
    coop_success = IntegerField(verbose_name="合作完成次数", null=False, default=0)
    coop_two = IntegerField(verbose_name="2次合作次数", null=False, default=0, help_text="如果合作2次成功以上这里才修改")

    update_at = DateTimeField(verbose_name="报表更新时间", null=True)
    year_amount = DecimalField(verbose_name="一年内收总金额", null=False, max_digits=10, decimal_places=2, default=0)
    season_invite = IntegerField(verbose_name="90天内被邀请", null=False, default=0)
    season_reply = IntegerField(verbose_name="90内回复", null=False, default=0)
    season_day_reply = IntegerField(verbose_name="90天内当天回复", null=False, default=0)
    season_proposal = IntegerField(verbose_name="90天内投标", null=False, default=0)
    season_view = IntegerField(verbose_name="90天内被查看", null=False, default=0)
    season_interview = IntegerField(verbose_name="90天内沟通中", null=False, default=0)
    season_hire = IntegerField(verbose_name="90天内被雇佣", null=False, default=0)

    class Meta:
        db_table = "user_statistics"

class UserDiscover(BaseModel):
    # 被发现及查看记录，每用户每天一条
    user = ForeignKeyField(User, related_name="discover")
    discover_num = IntegerField(verbose_name="被发现次数", null=False, default=0)
    view_num = IntegerField(verbose_name="被查看次数", null=False, default=0)
    period = IntegerField(verbose_name="日期", null=False, default=0)
    update_at = DateTimeField(verbose_name="报表更新时间", null=False)

    class Meta:
        db_table = "user_discover"
