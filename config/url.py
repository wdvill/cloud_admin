#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers import (
    page, user, sms, job, category, attachment, resume,
    address, margin, question, favorite, proposal,
    contract, freelancer, client, friend, notify,
    help_center, order, mobile)

urls=[
    ("/", page.Index),
    ("/find-work-home", job.JobHome),
    ("/signup", user.Signup),
    ("/signup-client", user.SignupClient),
    ("/signup-role", user.SignupRole),
    ("/signin", user.Signin),
    ("/signout", user.Signout),
    ("/forgotpassword",  user.ForgotPassword),
    ("/forgotpassword/success",  user.ForgotPasswordSuccess),
    ("/about", page.About),
    ("/help", help_center.Help),
    ("/help/topic/(\d+)", help_center.HelpTopic),
    ("/help/([0-9a-f]{16,16})", help_center.HelpDetail),
    ("/jump",   user.ClientJump),
    ("/desktop", page.Desktop),
    ("/download", page.Download),
    ("/concatus", page.ConcatUs),
    ("/joinus", page.JoinUs),

    ("/browse", page.Browse),
    ("/browse/jobs", job.IndexJobFind),
    ("/browse/freelancers", client.IndexFreelancerFindView),
    ("/messages/", page.Messages),

    ("/settings",   user.SettingsRedirect),

    ("/settings/account", freelancer.FreelancerSettingAccount),
    ("/settings/cards", freelancer.FreelancerSettingCards),
    ("/settings/alipay", freelancer.FreelancerSettingAlipay),
    ("/settings/password", freelancer.FreelancerSettingsPwd),
    ("/settings/question", freelancer.FreelancerSettingsQuestion),
    ("/settings/recharge", freelancer.FreelancerSettingRecharge),

    ("/freelancers/settings", freelancer.FreelancerSettings),
    ("/freelancers/settings/withdrawal", freelancer.FreelancerSettingWithdrawal),
    ("/freelancers/settings/concatinfo", freelancer.FreelancerSettingsInfo),
    ("/freelancers/settings/profile", freelancer.FreelancerSettingProfile),
    ("/freelancers/settings/identity", freelancer.FreelancerIdentity),
    ("/freelancers/settings/teams", freelancer.FreelancerSettingTeam),

    ("/freelancers/favorite", freelancer.FreelancerFavorite),
    ("/freelancers/subscribe", freelancer.FreelancerSubscribe),
    ("/freelancers/proposal", freelancer.FreelancerProposal),
    ("/freelancers/proposal/(\d+)", freelancer.FreelancerProposalDetail),

    ("/users/guide", user.Guide),
    ("/users/profile/step/1", user.FreelancerCategoryCreate),
    ("/users/profile/step/2", user.FreelancerProfileCreate),
    ("/users/profile/step/3", user.FreelancerWorkAndEduCreateView),
    ("/users/profile/step/4", user.FreelancerOtherCreateView),
    ("/users/profile/step/complete", user.FreelancerRegCompleteView),

    ("/users/role", user.UserRoleChange),

    ("/users/c/([0-9a-f]{16,16})", user.ChangeClient),
    ("/users/f/([0-9a-f]{16,16})", user.ChangeFreelancer),
    # 支付宝页面跳转回调
    ("/users/margin/deposit", margin.DepositCallback),

    ("/jobs/new", job.JobNew),
    ("/jobs/new/complete/([0-9a-f]{16,16})", job.JobNewComplete),
    ("/jobs/find", job.JobFind),
    ("/jobs/([0-9a-f]{16,16})",  job.JobDetail),
    ("/jobs/([0-9a-f]{16,16})/edit",  job.JobEditView),
    ("/jobs/([0-9a-f]{16,16})/proposal", job.JobFreelancerProposal),

    ("/freelancers/contracts/([0-9a-f]{16,16})", freelancer.ContractDetailView),
    ("/contracts/([0-9a-f]{16,16})/evaluate", client.ContractEvaluate),
    ("/contracts/([0-9a-f]{16,16})/feedback", client.ContractFeedback),
    ("/freelancers/contracts/([0-9a-f]{16,16})/(\d+)/complete", freelancer.ContractComplete),
    ("/freelancers/contracts/([0-9a-f]{16,16})/(\d+)/detail", freelancer.ContractDetail),

    #("/freelancers/contracts/([0-9a-f]{16,16})/diary", freelancer.WeekStoneDiaryView),

    ("/contracts/([0-9a-f]{16,16})/diary/(\d+)", freelancer.WeekStoneDiaryDetailView),

    ("/freelancers/find", client.FreelancerFindView),

    ("/freelancers/jobs", freelancer.JobsView),
    ("/freelancers/stats", freelancer.StatsView),
    ("/freelancers/contracts", freelancer.ContractsView),
    ("/freelancers/client/new", freelancer.CreateClientView),
    ("/freelancers/reports", freelancer.ReportView),
    ("/freelancers/diary", freelancer.DiaryView),
    ("/freelancers/([0-9a-f]{16,16})", freelancer.FreelancerDetail),
    ("/freelancers/offer/([0-9a-f]{16,16})", freelancer.OfferDetailView),
    ("/freelancers/([0-9a-f]{16,16})/invite", client.FreelancerInviteView),
    ("/freelancers/settings/notify", notify.NotifySettings),

    ("/clients/guide", client.GuideView),

    ("/clients/jobs", client.JobsView),
    ("/clients/jobs/list", client.JobsListView),
    ("/clients/freelancers", client.FreelancerView),
    ("/clients/freelancers/favorite", client.FreelancerSavedView),
    ("/clients/freelancers/hire", client.FreelancerHiredView),
    ("/clients/freelancers/waiting", client.FreelancerWaitView),
    ("/clients/freelancers/diary", client.DiaryView),

    ("/clients/contracts", client.ContractsView),
    #("/clients/contracts/([0-9a-f]{16,16})/pay", contract.ContractPay),
    ("/clients/offer/([0-9a-f]{16,16})/([0-9a-f]{16,16})/direct", client.OfferNewDirectView),
    ("/clients/contracts/([0-9a-f]{16,16})/pay", client.ContractPayView),
    ("/clients/contracts/([0-9a-f]{16,16})/active", client.ContractPayActive),  
    #("/clients/contracts/([0-9a-f]{16,16})/diary", client.WeekStoneDiaryView),
    ("/contracts/([0-9a-f]{16,16})/(milestone|weekstone|bonus)/([0-9]{18,18})", order.OrderPayView),
    ("/clients/contracts/([0-9a-f]{16,16})/milestone/add", client.ContractAddMilestone),  


    ("/clients/reports", client.StatsView),
    ("/clients/reports/weekly", client.StatsWeeklyView),
    ("/clients/reports/timesheet", client.StatsTimeSheetView),
    ("/clients/reports/budget", client.StatsBudgetView),
    ("/clients/reports/trade", client.StatsTradeView),

    ("/clients/jobs/([0-9a-f]{16,16})", client.ProposalView),
    ("/clients/proposal/(\d+)/offer", client.OfferNewView),

    ("/clients/settings", client.Settings),
    ("/clients/settings/identify", client.IndentifySettings),
    ("/clients/settings/conidentify", client.ConIndentifySettings),
    ("/clients/settings/notify", notify.NotifySettings),
    ("/clients/freelancer/new", client.CreateFreelancerView),
    ("/notify", notify.NotifyView),


    ("/mobile/concatus", mobile.Concatus),

    #用户协议
    ("/legal", page.Legal),
    #隐私政策
    ("/legal/privacy", page.Privacy),

    ("/api/device/version", page.AppVersion),
    ("/api/user/signup", user.Register),
    ("/api/user/signin", user.Login),
    ("/api/user/signout", user.Logout),
    ("/api/user/password/reset", user.PasswordReset),
    ("/api/user/password/change", user.PasswordChange),
    ("/api/user/password/verify", user.PasswordVerify),

    ("/api/user/category", user.FreelancerCategory),
    ("/api/user/profile", user.UserProfile),

    ("/api/user/other/create",    user.FreelancerOtherCreate),
    ("/api/user/resume", user.FreelancerWorkAndEduCreate),
    #("/api/user/profile/complete", user.FreelancerRegComplete),

    ("/api/user/client", user.CreateClient),
    ("/api/user/freelancer", user.CreateFreelancer),
    ("/api/user/verify", user.UserVerify),
    ("/api/user/role", user.UserRole),
    ("/api/user/alipay", user.UserAlipay),

    ("/api/user/jumpcode",  user.GetJumpCode),

    ("/api/verifycode", sms.SendVerifyCode),
    ("/api/jobs/search", job.JobSearch),
    ("/api/jobs", job.JobSet),
    ("/api/jobs/status", job.JobStatus),
    ("/api/jobs/proposal", job.JobProposal),
    ("/api/jobs/freelancers/recommand", job.FreelancerRecommand),
    ("/api/jobs/my", job.MyJobList),

    ("/api/category", category.CategoryList),
    ("/api/category/options", category.CategoryOptions),
    ("/api/skills", page.AllSkills),
    ("/api/address", address.AddressRecord),

    ("/api/question", question.QuestionRecord),
    ("/api/user/question", user.UserQuestion),

    ("/attachment/([0-9A-Fa-f]{32,32})", attachment.Download),
    ("/api/attachment", attachment.Upload),
    ("/api/employment", resume.Employment),
    ("/api/education", resume.Education),
    ("/api/portfolio", resume.Portfolio),

    ("/api/margin/basic", margin.BasicInfo),
    ("/api/margin/record", margin.Record),
    ("/api/margin/bank", margin.Bank),
    ("/api/margin/card", margin.BankCard),
    ("/api/margin/deposit", margin.Deposit),
    ("/api/margin/deposit/callback", margin.DepositCallbackSync),
    ("/api/margin/withdraw", margin.Withdraw),
    ("/api/margin/withdraw/accounts", margin.WithdrawAccounts),

    ("/api/favorite", favorite.Favorite),
    ("/api/subscribe", favorite.Subscribe),

    ("/api/proposal", proposal.Proposal),
    ("/api/proposal/im", proposal.ProposalBasic),
    ("/api/proposal/message", proposal.ProposalMessage),
    ("/api/contract", contract.Contract),
    ("/api/contract/basic", contract.ContractBasic),
    ("/api/contract/freelancers", contract.ContractFreelancers),
    ("/api/contract/evaluate", contract.Evaluate),
    ("/api/milestone", contract.MileStone),
    ("/api/milestone/pay", contract.MileStonePay),
    ("/api/contract/weekstone", contract.ContractWeekStoneList),
    ("/api/contract/bonus", contract.ContractSendBonus),

    #("/api/weekstone", contract.WeekStone),
    ("/api/weekstone/time", contract.WeekStoneTime),
    ("/api/weekstone/pay", contract.WeekStonePay),
    ("/api/weekstone/screenshot", contract.WeekStoneShot),
    ("/api/freelancers/search", client.FreelancerSearch),
    ("/api/freelancers/contract", freelancer.FreelancerContract),
    ("/api/freelancers/recommand", freelancer.FreelancerRecommand),

    ("/api/friends", friend.FriendList),
    ("/api/friends/users", friend.FriendUsersList),

    ("/api/e/session", user.IMSessionVerify),
    ("/api/d/weekstone", contract.DesktopWeekStone),

    ("/api/d/network", page.DesktopNetwork),

    ("/api/client/verify", client.ClientVerify),
    ("/api/client/freelancers", client.FreelancerList),

    ("/api/stats/weekly", client.WeeklySummary),
    ("/api/stats/budget",  client.StatsBudget),
    ("/api/stats/timesheet", client.TimeSheet),
    
    # 开发者报表
    ("/api/stats/freelancer", freelancer.FreelancerStats),
    ("/api/stats/statis", freelancer.FreelancerTongji),

    ("/api/banners", page.Banner),
    ("/api/notify", notify.Notify),
    ("/api/feedback", page.Feedback),
    ("/api/notify/setting", notify.NotifyUserSetting),

    ("/api/freelancers/discover", freelancer.DiscoverView),
    ("/api/order/pay", order.OrderPayApi),
    # 添加一个临时测试提审时薪入口
    ("/api/test/contract/weekstone/audit", contract.TestContractWeekStoneAudit),

    ("/(.*)", page.NotFound)
]
