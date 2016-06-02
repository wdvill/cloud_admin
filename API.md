Cloudwork 2.0 API Reference
=================

说明
------

1. 此文档不包括web页面接口，返回值均为json,需要进行序列化，且error_code字段为必须，如error_code=0则表示接口请求成功

2. APP需要定义User-Agent, User-Agent格式如下:

		类型/app版本号/系统版本号/设备名/网络状态(i/1.0.0/9.2.1/iPhone/wifi)其中第一个字段i表示ios，a表示安卓, w表示winphone
3. Web端除了GET接口，都需要传递`_xsrf`参数，此参数通过`Cookie.get(_xsrf)`获取
4. Web端不需要显式传递`session_token`参数，服务端会通过请求的`Cookie`获取，APP需要显式传递此参数
5. 需要登录才能访问的接口会标示。
6. 暂时工作,用户,合同的id不会返回，返回的是uuid代表id。
7. App假如本地缓存的错误码json文件有未找到的错误时，再请求新的json文件。地址: http://$host/static/locale-zh-cn.json
8. App获取接口，错误码30001=>当前不是需求者，30002=>当前不是服务方
9. 桌面端无论什么身份，都认为是开发者调用接口。(以/d开头的user-agent)

<div id="interface"/>
## 接口文档列表 Table of content

| 接口名 | 接口名 | 接口名 | 接口名 | 接口名 |
|:---:|:---:|:---:|:---:|:---:|
|[登录](#signin)|[注册](#signup)|[退出](#signout)|[忘记密码/密码重置](#forgotpassword)|[获取短信验证码](#verifycode)|
|[APP客户端升级](#version)|[上传附件/头像](#attachment)|[用户实名认证](#verify)|[工作经历查询](#employment_get)|[工作经历新增](#employment_add)|
|[工作经历修改](#employment_update)|[工作经历删除](#employment_del)|[教育经历查询](#education_get)|[教育经历新增](#education_add)|[教育经历修改](#education_update)|
|[教育经历删除](#employment_del)|[项目经历查询](#portfolio_get)|[项目经历新增](#portfolio_add)|[项目经历修改](#portfolio_update)|[项目经历删除](#portfolio_del)|
|[需求者发布项目](#jobs_add)|[搜索项目](#jobs_search)|[分页获取项目列表](#jobs_get)|[国家省市列表](#address_get)|[获取分类目录](#category)|
|[更新用户分类](#category_update)|[获取用户个人信息](#profile_get)|[修改用户个人详细信息](#profile_update)|[查询用户角色](#role_get)|[用户角色切换](#role_update)|
|[修改密码](#password_change)|[问题列表](#question_list)|[用户密保问题列表](#question_get)|[创建用户密保问题](#question_add)|[修改用户密保问题](#question_update)|
|[创建一个需求者](#client_add)|[根据ID获取需求者信息](#client_get)|[收藏项目列表](#favorite_get)|[收藏](#favorite_add)|[取消收藏](#favorite_del)|
|[创建用户分类(完善资料1)](#category_add)|[创建用户个人详细信息(完善资料2)](#profile_add)|[完善经历(完善资料3)](#user_resume)|[创建用户时薪等信息(完善资料4)](#profile_other)||
|[查询招投标](#proposal_list)|[招投标](#proposal)|[投标操作](#proposal_update)|[创建支付宝账号](#alipay_create)|[删除支付宝账号](#alipay_delete)
|[银行列表](#margin_bank)|[银行卡列表](#margin_card)|[账户变动记录](#margin_record)|[账户余额](#margin_basic)|[查询项目合同](#jobs_proposal)|
|[查询订阅](#subscribe_list)|[订阅](#subscribe_create)|[取消订阅](#subscribe_delete)|[超时验证密码](#password_verify)|[创建合同/发offer](#contract_create)|
|[接受/拒绝offer](#a_r_contract)|[合同撤消/暂停/重新开始](#revoke_contract)|[查询合同](#contract_list)|[结束合同](#finish_contract)|[项目状态变更](#jobs_close)|
|[里程碑查询](#milestone_list)|[里程碑创建](#milestone_create)|[里程碑提审、审核](#milestone_update)|[根据id查询项目](#jobs_one)|[付款申请查询](#milestone_pay)|
|[获取用户分类](#category_users)|[搜索开发者](#freelancer_search)|[需求者发布项目数据统计](#user_statistics)|[用户充值](#margin_deposit)|[用户提现账户查询](#withdraw_account)|
|[提现](#withdraw)|[添加银行卡](#card_add)|[删除银行卡](#card_del)|[创建开发者身份](#create_freelancer)|[需求者企业认证](#client_verify)|
|[需求者雇佣列表](#client_freelancer_list)|[任务发布完推荐10位](#job_freelancer_recom)|[开发者报表](#freelancer_stats)|[需求者预算报表](#client_stats_budget)|[需求者周报报表](#client_stats_weekly)|
|[需求者交易记录报表](#client_stats_marginrecord)|[合同开发者查询](#contract_freelancers)|[创建一条截屏记录](#weekstoneshot)|[获取Banner](#banners)|[发送投标消息](#proposal_msg_send)|
|[获取投标消息](#proposal_msg_list)|[消息列表](#notify_list)|[消息更新已读](#notify_update)|[消息删除](#notify_delete)|[查询开发者工作经历](#freelancer_contract)|
|[获取我的工作列表](#my_jobs_list)|[为开发者推荐开发者](#freelancer_recommend)|[获取登录跳转码](#get_jump_code)|[登录跳转](#jump_code_jump)|[获取好友列表](#get_friends_list)|
|[获取好友用户信息](#get_friends_user_info)||[提交反馈](#new_feedback)|[获取截屏记录](#get_weekstoneshot)|[结束合同评价](#contract_evaluate)|
|[获取合同列表](#get_contract_basic)||[获取当前工作时长](#get_weekstone_time)|[获取付款时薪信息](#get_weekstone_pay)|[时薪里程碑审核](#weekstone_audit)|
|[时薪里程碑开启](#weekstone_create)|[桌面端获取时薪合同](#desktop_weekstone_list)|[工作日志查询列表](#contract_weekstone_list)|[奖金订单创建](#bonus_create)|[奖金订单支付](#bonus_pay)|
|[更新工作日志截屏备注](#weekstoneshot_update)|[删除工作日志截屏](#weekstoneshot_del)|[奖金订单查询](#bonus_query)|[通知设置](#notify_setting)|[获取统计数据](#get_statis)|
|[需求者工时报表](#client_stats_timesheet)|[删除工作](#job_delete)|[支付订单查询](#get_pay_order)|[支付订单支付](#order_payment)|[获取分类选项](#category_options)|
|[需求者修改项目](#jobs_update)|[截屏记录详情](#shot_one)||||

<div id="signin"/>[TOP^](#interface)
### <font color=blue>登录</font>
    POST /api/user/signin

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|username|String|是|用户名(`username`,`phone`,`email`)|
|password|String|是|用户密码|
|remember|Boolean|否|是否记住登录状态(true,false)|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|session_token|String|登录成功标识|
|expire_at|Datetime|session过期时间|
|identify|String|上次退出时的身份.<br/>1: 需求者个人<br/>2: 需求者企业<br/>3: 开发者|


<div id="signup"/>[TOP^](#interface)
### <font color=blue>注册</font>
    POST /api/user/signup

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|rtype|String|是|注册类型<br/>开发者个人:1<br/>需求者企业:2<br/>需求者个人:3|
|name|String|是|真实姓名|
|phone|Int|是|手机号|
|password|String|是|密码，长度在4-20位|
|vcode|Int|是|短信验证码(6位数字)|
|username|String|否|用户名(现阶段开发者注册不在使用此字段)|
|country|String|否|国家|
|cname|String|否|需求者企业名称|
|notice|Boolean|是|是否接收推荐通知|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="signout"/>[TOP^](#interface)
### <font color=blue>退出</font>
    POST /api/user/signout

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|session_token|String|是|session参数|

<font color=red>注: Web端调用GET /signout ，无须传参</font>

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="forgotpassword"/>[TOP^](#interface)
### <font color=blue>忘记密码/密码重置</font>
	POST /api/user/password/reset

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|username|String|是|用户名|
|password|String|是|新密码|
|vcode|Int|是|手机短信验证码|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="verifycode"/>[TOP^](#interface)
### <font color=blue>获取短信验证码</font>
	POST /api/verifycode

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|vtype|String|是|验证码类型<br/>enter:已经登录用户获取验证码<br/>register:注册获取验证码<br/>forget:忘记密码获取验证码<br/>|
|phone|Int|否|手机号(若输入注册标志，此项为用户名)|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|vcode|Int|验证码|


<div id="version"/>[TOP^](#interface)
### <font color=blue>APP客户端升级</font>
	POST /api/device/version

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|data|String|版本更新信息|

Desktop update
```
data as json: {
    lastest_version: '1.0.0',
    dl_url: '下载链接(会交给浏览器打开,可以是文件也可以是itunes的链接)',
    note: '升级提示',
}
```


<div id="attachment"/>[TOP^](#interface)
### <font color=blue>上传附件/头像</font>
	POST /api/attachment

登录: 是

权限: 需求者/开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|file|file|是|请示body体为文件内容,以file为键|
|t|String|是|上传类型<br/>avatar:头像<br/>logo:企业logo<br/>job:工作<br/>contract:合同<br/>milestone:里程碑<br/>proposal:投标<br/>portfolio:项目经历<br/>shot:截屏，按小时计费监测<br/>company:公司信息<br/>|
|x|Int|否|若t=avatar或者logo,必须|
|y|Int|否|若t=avatar或者logo,必须|
|w|Int|否|若t=avatar或者logo,必须|
|h|Int|否|若t=avatar或者logo,必须|
|boundx|Int|否|若t=avatar或者logo,必须|
|boundy|Int|否|若t=avatar或者logo,必须|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|attachment_id|Int|文件ID|
|name|String|文件名称|
|path|String|文件绝对路径|
|md5|String|md5值|
|size|Int|文件大小|


<div id="category"/>[TOP^](#interface)
### <font color=blue>获取分类目录</font>
	POST /api/category

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|category_id|Int|是|获取一级分类为0,获取子类别传一级ID|
|t|String|否|固定值`all`,获取全部分类|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|categorys|Array|类别数组|


<div id="employment_get"/>[TOP^](#interface)
### <font color=blue>工作经历查询</font>
	GET /api/employment

登录: 是

权限: 开发者、需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|否|不传则查询用户所有经历|
|user_id|String|否|开发者UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|employments|Array|工作经历列表|


<div id="employment_add"/>[TOP^](#interface)
### <font color=blue>工作经历新增</font>
    POST /api/employment

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|company|String|是|公司名称|
|city_id|Int|是|此工作所在城市ID|
|title|String|是|工作职位|
|role|Int|是|身份角色<br/>1: Intern<br/>2: General staff<br/>3: Charger<br/>4: Manager<br/>5: General manager<br/>6: Founder|
|start_at|String|是|工作开始日期, 格式yyyy-MM|
|end_at|String|是|工作截止日期，格式yyyy-MM|
|working|Boolean|是|是否在职, true, false|
|detail|String|否|工作细节|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|employment_id|Int|成功返回工作经历ID|


<div id="employment_update"/>[TOP^](#interface)
### <font color=blue>工作经历修改</font>
    PUT /api/employment

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|是|工作经历ID|
|company|String|是|公司名称|
|city_id|Int|是|此工作所在城市ID|
|title|String|是|工作职位|
|role|Int|是|身份角色<br/>1: Intern<br/>2: General staff<br/>3: Charger<br/>4: Manager<br/>5: General manager<br/>6: Founder|
|start_at|String|是|工作开始日期, 格式yyyy-MM|
|end_at|String|是|工作截止日期，格式yyyy-MM|
|working|Boolean|是|是否在职, true, false|
|detail|String|是|工作细节|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="employment_del"/>[TOP^](#interface)
### <font color=blue>工作经历删除</font>
    DELETE /api/employment

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|是|工作经历ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="education_get"/>[TOP^](#interface)
### <font color=blue>教育经历查询</font>
    GET /api/education

登录: 是

权限: 开发者、需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|否|教育经历id, 不传则获取用户所有教育经历列表|
|user_id|String|否|开发者UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|educations|Array|json数组，教育经历列表|


<div id="education_add"/>[TOP^](#interface)
### <font color=blue>教育经历新增</font>
    POST /api/education

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|start_at|String|是|开始日期，格式yyyy|
|end_at|String|是|结束日期，格式yyyy|
|school|String|是|学校|
|degree|String|是|学位，senior: 高中<br/>college: 大专<br/>bachelor: 本科<br/>master: 硕士<br/>mba: MBA<br/>emba: EMBA<br/>doctor: 博士<br/>others: 其他|
|area|String|否|专业|
|detail|String|否|简介|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|education_id|Int|成功返回教育经历ID|


<div id="education_update"/>[TOP^](#interface)
### <font color=blue>教育经历修改</font>
    PUT /api/education

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|是|教育经历ID|
|start_at|String|是|开始日期，格式yyyy|
|end_at|String|是|结束日期，格式yyyy|
|school|String|是|学校|
|degree|String|是|学位，senior: 高中<br/>college: 大专<br/>bachelor: 本科<br/>master: 硕士<br/>mba: MBA<br/>emba: EMBA<br/>doctor: 博士<br/>others: 其他|
|area|String|否|专业|
|detail|String|否|简介|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="employment_del"/>[TOP^](#interface)
### <font color=blue>教育经历删除</font>
    DELETE /api/employment

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|eid|Int|是|教育经历ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="portfolio_get"/>[TOP^](#interface)
### <font color=blue>项目经历查询</font>
    GET /api/portfolio

登录: 是

权限: 开发者、需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|pid|Int|否|项目经历ID|
|user_id|String|否|开发者UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|portfolios|Array|json数组|


<div id="portfolio_add"/>[TOP^](#interface)
### <font color=blue>项目经历新增</font>
    POST /api/portfolio

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|name|String|是|项目名称|
|category_id|Int|是|项目类别ID|
|detail|String|是|项目简介|
|end_at|String|否|完成日期，格式yyyy-MM|
|link|String|否|项目链接|
|picture_id|Int|否|项目图片，以附件形式上传后的ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|portfolio_id|Int|成功返回项目经理ID|


<div id="portfolio_update"/>[TOP^](#interface)
### <font color=blue>项目经历修改</font>
    PUT /api/portfolio

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|pid|Int|是|项目经历ID|
|name|String|是|项目名称|
|category_id|Int|是|项目类别ID|
|detail|String|是|项目简介|
|end_at|String|否|完成日期，格式yyyy-MM|
|link|String|否|项目链接|
|picture_id|Int|否|项目图片，以附件形式上传后的ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="portfolio_del"/>[TOP^](#interface)
### <font color=blue>项目经历删除</font>
    DELETE /api/portfolio

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|pid|Int|是|项目经历ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="jobs_add"/>[TOP^](#interface)
### <font color=blue>需求者发布项目</font>
    POST /api/jobs

登录: 是

权限: 需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|name|String|是|项目名称|
|description|String|是|项目简介|
|category_id|Int|是|项目分类|
|hires|Int|是|此项目招聘人数|
|paymethod|String|是|付款方式，因为选择<br/>hour: 按小时付费<br/>fixed: 固定金额|
|level|String|是|此项目需要经验级别<br/>entry: 入门级<br/>middle: 中间级<br/>expert: 专家级|
|duration|Int|否|此项目需要持续时间<br/>1: 大于6个月<br/>2: 3到6个月<br/>3: 1到3个月<br/>4: 不到1个月<br/>5: 小于1周|
|workload|Int|否|每周工作时间,按小时必须<br/>1: 超过30小时<br/>2: 小于30小时<br/>3: 不确定|
|attachment_id|Int|否|附件|
|api|String|否|是否集成API, social, pay, storage, other|
|platforms|String|否|适用平台，以逗号分隔，android,iphone,ipad,winphone,windows,linux,mac,other|
|frameworks|String|否|需要使用的框架,以逗号分隔|
|languages|String|否|需要具备语言能力,以逗号分隔|
|skills|String|否|技能，以逗号分隔|
|budget|Float|否|项目预算|
|stage|String|否|项目处于什么阶段<br/>design:设计<br/>introduction:说明书<br/>idea:不错的想法<br/>none:我不知道|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|job_id|String|成功返回项目UUID|


<div id="jobs_update"/>[TOP^](#interface)
### <font color=blue>需求者修改项目</font>
    PUT /api/jobs

登录: 是

权限: 需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|job_id|String|是|Job的UUID|
|name|String|是|项目名称|
|description|String|是|项目简介|
|category_id|Int|是|项目分类|
|hires|Int|是|此项目招聘人数|
|paymethod|String|是|付款方式，因为选择<br/>hour: 按小时付费<br/>fixed: 固定金额|
|level|String|是|此项目需要经验级别<br/>entry: 入门级<br/>middle: 中间级<br/>expert: 专家级|
|duration|Int|否|此项目需要持续时间<br/>1: 大于6个月<br/>2: 3到6个月<br/>3: 1到3个月<br/>4: 不到1个月<br/>5: 小于1周|
|workload|Int|否|每周工作时间,按小时必须<br/>1: 超过30小时<br/>2: 小于30小时<br/>3: 不确定|
|attachment_id|Int|否|附件|
|api|String|否|是否集成API, social, pay, storage, other|
|platforms|String|否|适用平台，以逗号分隔，android,iphone,ipad,winphone,windows,linux,mac,other|
|frameworks|String|否|需要使用的框架,以逗号分隔|
|languages|String|否|需要具备语言能力,以逗号分隔|
|skills|String|否|技能，以逗号分隔|
|budget|Float|否|项目预算|
|stage|String|否|项目处于什么阶段<br/>design:设计<br/>introduction:说明书<br/>idea:不错的想法<br/>none:我不知道|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|job_id|String|成功返回项目UUID|

<div id="jobs_search"/>[TOP^](#interface)
### <font color=blue>搜索项目</font>
    POST /api/jobs/search

权限: 无

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|workload|String|否|每周工作时间，以逗号分，如1,2,3<br/>1: 超过30小时<br/>2: 30小时以内<br/>3: 不确定|
|duration|String|否|项目持续时间，以逗号分隔，如1,2,3,4<br/>1: 大于6个月<br/>2: 3到6个月<br/>3: 1到3个月<br/>4: 不到1个月<br/>5: 小于1周|
|level|String|否|项目需要经验，以逗号分隔，如entry,middle<br/>entry: 入门级<br/>middle: 中间级<br/>expert: 专业级|
|paymethod|String|否|付款方式，以逗号分隔，如hour,fixed|
|pagesize|Int|否|每页获取条数|
|pagenum|Int|否|获取的页数|
|categorys|String|否|分类ID，以逗号分隔，如1,2,3|
|keyword|String|否|关键字|
|budget_range|String|否|预算区间,以逗号分隔最小和最大, 如100,5000|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|count|Int|搜索到的项目总数|
|jobs|Array|json数组|
|pagenum|Int|当前页数|


<div id="jobs_one"/>[TOP^](#interface)
### <font color=blue>根据UUID查询项目</font>
    GET  /api/jobs

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|job_id|String|是|项目UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|jobs|Array|项目Json数组|


<div id="jobs_get"/>[TOP^](#interface)
### <font color=blue>分页获取项目列表</font>
    GET /api/jobs

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|pagesize|Int|否|每页条数|
|pagenum|Int|否|获取的页数|
|job_id|String|否|项目UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|count|Int|项目总数|
|jobs|Array|json数组|
|pagenum|Int|当前页数|


<div id="jobs_close"/>[TOP^](#interface)
### <font color=blue>项目状态变更</font>
    PUT /api/jobs/status

登录: 是

权限: 需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|job_id|String|是|项目UUID|
|status|String|是|变更项目状态<br/>normal:公开状态(草稿允许公开)<br/>close:关闭状态(公开和私有可以关闭)<br/>private:私有状态|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="address_get"/>[TOP^](#interface)
### <font color=blue>国家省市列表</font>
    GET /api/address

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|address_id|Int|是|地址信息ID|
|t|String|否|all,若为all,获取全部地址|
|cid|Int|否|国家id,若有，则查询国家下的所有省市|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|address|Array|json数组|

<div id="category_users"/>[TOP^](#interface)
### <font color=blue>获取用户分类</font>
    GET /api/user/category

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|||||


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|categorys|Array|json数组<br/>name, category_id, parent_name, parent_id|

<div id="category_add"/>[TOP^](#interface)
### <font color=blue>创建用户分类</font>
    POST /api/user/category

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|category|String|是|用户分类id,以逗号分隔，如1,2,3,4,5|


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="category_update"/>[TOP^](#interface)
### <font color=blue>更新用户分类</font>
    PUT /api/user/category

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|category|String|是|用户分类id,以逗号分隔，如1,2,3,4,5|


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="profile_get"/>[TOP^](#interface)
### <font color=blue>获取用户个人信息</font>
    GET /api/user/profile

登录：是

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|uuid|String|否|用户的uuid串|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|profile|dict|个人信息字典|


<div id="profile_add"/>[TOP^](#interface)
### <font color=blue>创建用户个人详细信息</font>
    POST /api/user/profile

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|title|String|是|自己职位描述|
|overview|String|是|详细介绍|
|email|String|是|邮箱|
|skills|String|是|技能，以逗号分隔|
|english|String|是|英语级别,如： 1.初级水平 2.可以对话 3.顺利沟通 4.母语或双语|
|other|String|是|其他语言dict<br/>如：`{"Chinese":1, "Japanese":2}`|
|workload|Int|是|每周可工作小时数，1,2,3|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="profile_update"/>[TOP^](#interface)
### <font color=blue>修改用户个人详细信息</font>
    PUT /api/user/profile

登录: 是

权限: 开发者,需求者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|name|String|否|真实姓名,开发者|
|email|String|否|邮箱,开发者|
|location|String|否|所在城市ID,开发者|
|address|String|否|地址,开发者|
|postcode|Int|否|邮编,开发者|
|available|Boolean|否|是否可以工作,开发者|
|workload|Int|否|每周工作时长,开发者|
|title|String|否|工作职位描述,开发者|
|overview|String|否|详细简介,开发者|
|hourly|Float|否|时薪,开发者|
|skills|String|否|技能，以逗号分隔,开发者|
|english|String|否|英语级别,开发者|
|other|String|是|其他语言dict<br/>如：`{"Chinese":1, "Japanese":2}`,开发者|
|level|String|否|经验级别,开发者|
|name|String|否|用户姓名,需求者|
|client_name|String|否|企业名称,需求者|
|link|String|否|企业网站,需求者|
|overview|String|否|企业简介,需求者|
|location_id|Int|否|企业城市,需求者|
|address|String|否|企业地址,需求者|
|phone|String|否|联系电话,需求者|
|email|String|否|联系邮箱,需求者|


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="profile_other"/>[TOP^](#interface)
### <font color=blue>创建用户时薪等信息</font>
    POST /api/user/other/create

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|amount|Float|否|时薪|
|location|Int|是|所在城市ID|
|address|String|是|地址|
|postcode|String|否|邮政编码|


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="password_change"/>[TOP^](#interface)
### <font color=blue>修改密码</font>
    POST /api/user/password/change

登录: 是

权限: 开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|password_old|String|是|原密码|
|password|String|是|新密码|


返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="question_list"/>[TOP^](#interface)
### <font color=blue>问题列表</font>
    GET /api/question

登录：是

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
| qtype | String | 是 | 问题类别<br/>user:保密问题<br/>proposal_revoke_f:撤销投标<br/>proposal_refuse_f:拒绝邀请<br/>proposal_refuse_c:拒绝投标<br/>contract_revoke:撤销合同问题<br/>contract_refuse:拒绝合同<br/>proposal_archive: 归档原因<br/>contract_finish_c:需求者结束合同<br/>contract_finish_f:开发者结束合同|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|questions|Array|json数组|


<div id="question_get"/>[TOP^](#interface)
### <font color=blue>用户密保问题列表</font>
    GET /api/user/question

登录：是

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
| | | | |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|questions|Array|json数组|


<div id="question_add"/>[TOP^](#interface)
### <font color=blue>创建用户密保问题</font>
    POST /api/user/question

登录：是

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|question_id|Int|是|密保问题ID|
|answer|String|是|答案|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="question_update"/>[TOP^](#interface)
### <font color=blue>修改用户密保问题</font>
    PUT /api/user/question

登录：是

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|question_id|Int|是|密保问题ID|
|answer|String|是|答案|
|answer_old|String|是|旧答案|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="client_add"/>[TOP^](#interface)
### <font color=blue>创建一个需求者</font>
    POST /api/user/client

登录: 是

权限：开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|name|String|是|需求者名字|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="client_get"/>[TOP^](#interface)
### <font color=blue>根据工作获取需求者简介信息</font>
    GET /api/user/client

登录: 是

权限：开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|team_id|String|是|team uuid|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|
|info|Dict|需求者简介信息，包括获取的评价数，总消费，总雇佣数|


<div id="verify"/>[TOP^](#interface)
### <font color=blue>用户实名认证</font>
    POST /api/user/verify

登录: 是

权限：开发者

| 参数名 | 参数类型 | 是否必须 | 描述 |
|:---:|:---:|:---:|:---|
|name|String|是|真实姓名|
|id_number|String|是|身份证号|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---|
|error_code|Int|错误码|
|msg|String|错误信息|


<div id="favorite_get"/>[TOP^](#interface)
### <font color=blue>收藏列表</font>
	GET /api/favorite

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| pagesize | Int | 否 | 每页条数 |
| pagenum | Int | 否 | 页码 |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| favorites | Array | json数组 |


<div id="favorite_add"/>[TOP^](#interface)
### <font color=blue>收藏</font>
	POST /api/favorite

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| target_id | Int | 是 | 目标uuid，需求方收藏服务方，服务房收藏项目 |
| memo | String | 否 | 收藏备注，需求者收藏开发者备注 |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="favorite_del"/>[TOP^](#interface)
### <font color=blue>取消收藏</font>
	DELETE /api/favorite

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| target_id | Int | 是 | 目标uuid，需求方收藏服务方，服务房收藏项目 |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="role_get"/>[TOP^](#interface)
### <font color=blue>查询用户角色</font>
	GET /api/user/role
	
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| | | |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| name | String | 名称 |
| role | String | 用户角色<br/>c：企业需求者<br/>f：个人开发者 |
| team_id | Int | 企业需求者ID |


<div id="role_update"/>[TOP^](#interface)
### <font color=blue>用户角色切换</font>
	PUT /api/user/role

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| id | String | 是 | 需求者或者开发者uuid |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="user_resume"/>[TOP^](#interface)
### <font color=blue>完善经历</font>
	POST /api/user/resume

登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|level|String|是|经验水平<br/>entry: 入门级<br/>middle: 中间级<br/>expert: 专业级|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="proposal_list"/>[TOP^](#interface)
### <font color=blue>查询招投标</font>
	GET /api/proposal

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| operate | String | 否 | 操作类型, operate/proposal_id/job_id 必输填写其中一项<br/>开发者操作类型如下:<br/>interview: 沟通中<br/>invite: 收到的邀请<br/>active: 待处理投标<br/>freeze: 冻结中<br/>需求者操作类型如下:<br/>active: 申请中<br/>interview:沟通中<br/>hire: 已雇佣<br/>archive: 已归档<br/>invite:需求者邀请开发者未处理|
| proposal_id |Int |  否 | 投标ID, operate/proposal_id/job_id 必输填写其中一项 |
| job_id | String | 否 | 项目UUID, operate/proposal_id/job_id 必输填写其中一项 |
| pagesize | Int | 否 | 每页条数 |
| pagenum | Int | 否 | 页码 |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| proposals | Array | 招投标列表 |


<div id="proposal"/>[TOP^](#interface)
### <font color=blue>招投标</font>
	POST /api/proposal

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|job_id|String|是|项目UUID|
|user_id|String|否|被邀请用户UUID，招标必输|
|amount|Float|否|投标金额，投标必输|
|duration|Int|否|预计完成时间，投标固定价格项目必输|
|message|String|否|信息，投标必输|
|attachment_id|Int|否|附件ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="proposal_update"/>[TOP^](#interface)
### <font color=blue>投标操作</font>
	PUT /api/proposal

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|proposal_id|Int|是|投标ID|
|operate|String|是|操作类型<br/>accept: 同意<br/>refuse: 拒绝<br/>revoke: 撤销<br/>hire: 雇佣(直接发送offer，不需要操作这个招投标)<br/>archive: 归档<br/>reactive: 重投<br/>unfreeze: 解冻<br/>|
|amount|Float|否|重投标金额|
|question_id|Int|否|拒绝原因|
|message|String|否|信息，备注|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="margin_bank"/>[TOP^](#interface)
### <font color=blue>银行列表</font>
	GET /api/margin/bank

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| banks | Array | Json数组，银行列表 |


<div id="margin_card"/>[TOP^](#interface)
### <font color=blue>银行卡列表</font>
	GET /api/margin/card

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| cards | Array | Json数组，银行卡列表 |


<div id="card_add"/>[TOP^](#interface)
### <font color=blue>添加银行卡</font>
	POST /api/margin/card

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|card_no|Int|是|银行卡号|
|code|String|是|银行代码|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| card_id| Int | 银行卡列表ID|


<div id="card_del"/>[TOP^](#interface)
### <font color=blue>删除银行卡</font>
	DEL /api/margin/card

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|card_id|Int|是|银行卡ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="margin_basic"/>[TOP^](#interface)
### <font color=blue>账户资金信息</font>
	GET /api/margin/basic

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

注: 服务方获取余额和收入，需求方获取累计支付和托管

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| margin | Float | 余额 |
| withdraw | Float| 体现中金额 |


<div id="margin_record"/>[TOP^](#interface)
### <font color=blue>账户变动记录列表</font>
	GET /api/margin/record

登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| rtype | String | 否 | 查询类型，默认为all<br/>pay:支付<br/>freeze:冻结<br/>refund:退款<br/>income:收入<br/>bonus:奖金<br/>|
| report | Boolean | 否 | 查询范围<br/>false:查询全部<br/>true:开发者/需求者报表查询, 只查询收入和奖金两种类型|
|start_at|Datetime|否|开始时间,需求者查询报表必输yyyy-mm-dd|
|end_at|Datetime|否|结束时间,需求者查询报表必输,yyyy-mm-dd|
|pagenum|Int|否|分也查询页号|
|pagesize|Int|否|分也查询，页大小|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| records | Array | Json数组 |
| count | Int | 总数 |
| pagenum | Int | 页码 |
| margin| Float | 余额,需求者报表查询返回|
| pay| Float | 支付金额,需求者报表查询返回|
| freeze | Float | 冻结金额,需求者报表查询返回|
| refund | Float | 退款金额,需求者报表查询返回|
| income | Float | 收入金额，开发者报表查询返回|


<div id="alipay_create"/>[TOP^](#interface)
### <font color=blue>创建支付宝账号</font>
    POST /api/user/alipay
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|alipay|String|是|支付宝账号|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="alipay_delete"/>[TOP^](#interface)
### <font color=blue>删除支付宝账号</font>
    DELETE /api/user/alipay
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="subscribe_list"/>[TOP^](#interface)
### <font color=blue>查询订阅</font>
    GET /api/subscribe
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| subscribes | Array | 订阅Json数组 |


<div id="subscribe_create"/>[TOP^](#interface)
### <font color=blue>订阅</font>
    POST /api/subscribe
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|name|String|是|订阅名称，最大20字符|
|duration|Int|否|此项目需要持续时间，以逗号分隔，如1,2,3,4,5<br/>1: 大于6个月<br/>2: 3到6个月<br/>3: 1到3个月<br/>4: 不到1个月<br/>5: 小于1周|
|workload|Int|否|每周工作时间，以逗号分隔，如1,2,3<br/>1: 超过30小时<br/>2: 小于30小时<br/>3: 不确定|
|paymethod|String|否|付款方式，以逗号分隔，如hour,fixed<br/>hour: 按小时付费<br/>fixed: 固定金额|
|level|String|否|此项目需要经验级别，以逗号分隔，如entry,middle,expert<br/>entry: 入门级<br/>middle: 中间级<br/>expert: 专家级|
|keyword|String|否|搜索关键字，小于30个字符|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="subscribe_delete"/>[TOP^](#interface)
### <font color=blue>取消订阅</font>
    DELETE /api/subscribe
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| subscribe_id | Int | 是 | 订阅ID | 

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="jobs_proposal"/>[TOP^](#interface)
### <font color=blue>查询项目合同</font>
    GET /api/jobs/proposal
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| jobs | Arrey | 项目信息Json数组 |


<div id="password_verify"/>[TOP^](#interface)
### <font color=blue>超时验证密码</font>
    POST /api/password/verify
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| password | String | 是 | 密码 |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="contract_list" />[TOP^](#interface)
### <font color=blue>合同列表查询</font>
    GET /api/contract
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|否|合同UUID|
|team_id|String|否|需求者团队uuid,获取团队合同列表需要此参数|
|pagesize|Int|否|每页获取条数|
|pagenum|Int|否|获取的页数|
|status|String|否|查询分类,如果输入contract_id或team_id则此字断非必输<br/>开发者查询类型如下:<br/>paid:待签约offer<br/>carry_fixed:固定价格合同<br/>carry_hour:时薪合同<br/>finish:已完成合同<br/>all:全部合同<br/>offer:全部offer<br/>需求者查询类型如下:<br/>carry:进行中的合同<br/>carry_pay:请求支付合同<br/>all:全部合同<br/>paid:待签约offer<br/>offer:全部offer<br/>|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
|contracts|Array|合同列表|
|count|Int|Int|数量|
|pagenum|Int|页码|


<div id="contract_create"/>[TOP^](#interface)
### <font color=blue>创建合同/发offer</font>
    POST /api/contract
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|user_id|String|是|发offer对象uuid|
|job_id|String|是|工作uuid|
|name|String|是|合同名字|
|amount|Float|是|合同金额|
|hourly|Float|否|时薪|
|workload|Int|否|每周工作小时，具体小时数，若时薪，此为必须|
|manual|Boolean|否|是否允许人工计时，true:是，false：否|
|message|String|否|留言|
|start_at|Datetime|否|开始时间,yyyy-mm-dd HH:MM:SS|
|end_at|Datetime|否|结束时间,yyyy-mm-dd HH:MM:SS|
|attachment_id|Int|否|附件id|
|milestones|Array|否|里程碑数组<br/>[{name:名称, amount:金额, end_at:结束时间}]

<font color=red>注: 或为固定工作，amount、start_at必须, 按小时工作,end_at必须,开始，结束时间必须大于当前时间</font>

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID |
| trade_no | String | 支付交易号 |


<div id="a_r_contract"/>[TOP^](#interface)
### <font color=blue>接受/拒绝offer</font>
    PUT /api/contract
登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同uuid|
|status|String|是|状态(accept, refuse)|
|question_id|Int|否|若拒绝必须,问题id|
|reason|String|否|拒绝/接受原因|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="revoke_contract"/>[TOP^](#interface)
### <font color=blue>合同撤消/暂停/重新开始</font>
    PUT /api/contract
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同uuid|
|status|String|是|状态(revoke, pause, carry)|
|question_id|Int|否|撤消合同使用|
|reason|String|否|撤消合同使用|

注：按小时工作重新开始，如果账户余额不足，可能会开启失败

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="finish_contract"/>[TOP^](#interface)
### <font color=blue>结束合同</font>
    PUT /api/contract
登录：是

权限：需求者/开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同uuid|
|status|String|是|状态(finish)|
|is_pay|Boolean|是|是否付款/不要款项,true, false|

<font color=red>注: 开发者结束合同,is_pay必须,哪个值都可以，后端不检查有效性</font>

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="milestone_list"/>[TOP^](#interface)
### <font color=blue>里程碑查询</font>
    GET /api/milestone
登录：是

权限：需求者／开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同UUID|
|milestone_id|Int |否|里程碑ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| milestones | Array | 里程碑Json数组 |


<div id="milestone_create"/>[TOP^](#interface)
### <font color=blue>里程碑创建</font>
    POST /api/milestone
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同UUID|
|milestones|Array|是|里程碑数组<br/>[{name:名称, amount:金额, end_at:结束时间}]

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID |
| trade_no | String | 支付交易号 |


<div id="milestone_update"/>[TOP^](#interface)
### <font color=blue>里程碑提审、审核</font>
    PUT /api/milestone
登录：是

权限：需求者\开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|milestone_id|Int|是|里程碑ID|
|attachment_id|Int|否|附件ID|
|message|String|否|消息|
|is_agree|String|否|需求者审核里程碑<br/>accept:同意<br/>refuse:拒绝<br/>release:主动释放<br/>|
|is_stop|Boolean|否|审核通过时，是否停止合同,需求者审核必输|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="milestone_pay"/>[TOP^](#interface)
### <font color=blue>付款申请查询</font>
    GET /api/milestone/pay
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同ID|

注：返回字段是records为数组，按时间降序排列

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| data | Dict | 数据 name, amount, end_at, user, records|

<div id="freelancer_search"/>[TOP^](#interface)
### <font color=blue>搜索开发者</font>
    GET /api/freelancers/search

权限：无

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|categorys|String|否|分类ID，以逗号分隔，如1,2,3|
|hourly_range|Int|否|时薪区间,0-4, 0和5以上都为全部|
|keyword|String|否|搜索关键字|
|coop_rate|Int|否|工作成功率, 具体数字，如80|
|pagenum|Int|否|默认为10|
|pagesize|Int|否|默认为1|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| users | Dict | 数据 name, amount, end_at, user, records|
| count|Int|总数|
|pagenum|Int|当前页|


<div id="user_statistics"/>[TOP^](#interface)
### <font color=blue>需求者发布项目数据统计</font>
    GET /api/user/statistics

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|team_id|String|是|项目UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| statistics | Array | 发标情况Json数组|


<div id="margin_deposit"/>[TOP^](#interface)
### <font color=blue>用户充值</font>
    POST /api/margin/deposit
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|amount|Float|是|充值金额|
|dtype|String|是|充值类型<br/>margin:充值默认是此类型<br/>contract:充值合同款<br/>bonus:发放奖金|
|contract_id|String|否|合同UUID，当为合同充值和发放奖金时必输|
|trade_no|String|否|发放奖金必输|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| url | String | 支付宝充值url |


<div id="withdraw_account"/>[TOP^](#interface)
### <font color=blue>用户提现账户查询</font>
    GET /api/margin/withdraw/accounts
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| accounts | Array | 支付Json数组 |


<div id="withdraw"/>[TOP^](#interface)
### <font color=blue>提现</font>
    POST /api/margin/withdraw
登录：是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|amount|Float|是|充值金额|
|account|String|是|账户号|
|type|String|是|账户类型<br/>alipay:支付宝<br/>bank:银行卡<br/>|
|code|Int|是|短信验证码|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| amount| Float | 提现金额 |
| balance | Float | 余额 |

<div id="create_freelancer"/>[TOP^](#interface)
### <font color=blue>创建开发者身份</font>
    POST /api/user/freelancer
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|||||

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="client_verify"/>[TOP^](#interface)
### <font color=blue>需求者企业认证</font>
    POST /api/client/verify
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|company_name|String|是|企业名称|
|name|String|是|联系人名称|
|phone|String|是|联系人电话|
|permit_number|String|是|营业执照号|
|org_number|String|是|组织机构代码|
|permit_id|Int|否|营业执照图片ID|
|org_id|Int|否|组织结构图片ID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="client_freelancer_list"/>[TOP^](#interface)
### <font color=blue>需求者雇佣的开发者列表</font>
    GET /api/client/freelancers
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|||||

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| users | Array | 用户列表 |

<div id="job_freelancer_recom"/>[TOP^](#interface)
### <font color=blue>任务发布完推荐10位</font>
    GET /api/jobs/freelancers/recommand
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|job_id|String|是|job_uuid|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| users | Array | 用户列表 |


<div id="freelancer_stats"/>[TOP^](#interface)
### <font color=blue>开发者报表查询</font>
    GET /api/stats/freelancers
登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|status|String|是|查询报表类型<br/>carry:进行中<br/>carry_pay:审核中<br/>|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| milestones | Array | 里程碑信息数组列表 |
| weekstones | Array | 按时计费合同列表 |
| amount_carry | Float | 进行中金额 |
| amount_carry_pay | Float | 审核中金额 |
| balance | Float | 可用余额 |


<div id="client_stats_budget"/>[TOP^](#interface)
### <font color=blue>需求者预算报表</font>
    GET /api/stats/budget
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|start_at|String|是|开始日期, 格式为yyyy-MM-dd|
|end_at|String|是|截止日期, 格式为yyyy-MM-dd|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contracts| Array | 固定价格合同信息 |


<div id="client_stats_timesheet"/>[TOP^](#interface)
### <font color=blue>需求者工时报表</font>
    GET /api/stats/timesheet
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|start_at|String|是|开始日期, 格式为yyyy-MM-dd|
|end_at|String|是|截止日期, 格式为yyyy-MM-dd|
| freelancer_id | String | 否 | 自由职业者UUID |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| weekstones | Array | 固定价格合同信息 |


<div id="client_stats_weekly"/>[TOP^](#interface)
### <font color=blue>需求者周报报表</font>
    GET /api/stats/weekly
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|start_at|String|是|开始日期, 格式为yyyy-MM-dd|
|end_at|String|是|截止日期, 格式为yyyy-MM-dd|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| weekstones | Array | 时薪里程碑 |
| milestones | Array | 固定价格里程碑 |
| bonus | Float | 奖金 ｜


<div id="contract_freelancers"/>[TOP^](#interface)
### <font color=blue>需求者查询已雇用开发者</font>
    GET /api/contract/freelancers
登录：是

权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|pagenum|Int|否|默认为10|
|pagesize|Int|否|默认为1|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| freelancers | Array | 开发者信息列表 |
| count | Int |  数据综述 |
| pagenum | Int | 页码 |


<div id="get_weekstoneshot"/>[TOP^](#interface)
### <font color=blue>获取截屏记录</font>
    GET /api/weekstone/screenshot
登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|shot_time|Datetime|是|截屏时间,日期，如:2016-04-05|
|contract_id|String|是|合同uuid|
|t|String|否|获取什么类型，目前只有一个last，获取上一条，当t不为空时，shot_time随便填|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
|shots|Array|截屏记录|

<div id="weekstoneshot"/>[TOP^](#interface)
### <font color=blue>上传一条截屏记录</font>
    POST /api/weekstone/screenshot
登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| name | String | 是 | 截屏名称|
|shot_time|Datetime|是|截屏时间|
|description|String|是|描述|
|activity|Int|是|0-100数字，活跃度|
|keyboard|Int|是|敲键盘次数|
|mouse|Int|是|点击鼠标次数|
|contract_id|String|是|合同uuid|
|attachment_id|Int|是|附件id|
|is_auto|String|否|是否手动,1自动，0手动|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="weekstoneshot_update"/>[TOP^](#interface)
### <font color=blue>更新截屏备注</font>
    PUT /api/weekstone/screenshot
登录：是

权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|shot_ids|String|是|以逗号分隔的列表，如1,2,3,4|
|name|String|是|备注名|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="weekstoneshot_del"/>[TOP^](#interface)
### <font color=blue>删除工作日志截屏</font>
    DELETE /api/weekstone/screenshot
登录：是


| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|shot_ids|String|是|截屏记录id, 如1,2,22,3,5|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="banners"/>[TOP^](#interface)
### <font color=blue>获取APP的Banner图</font>
    GET /api/banners

权限：无

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| platform | String | 否 | app: 各个端<br/>ios: iphone<br/>android |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| banners | Array | 开发者信息列表 |

<div id="proposal_msg_send"/>[TOP^](#interface)
### <font color=blue>发送投标消息</font>
    POST /api/proposal/message

登录: 是

权限：无

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| proposal_id | Int | 否 | 投标ID |
| contract_id | Int | 否 | 合同UUID |
| content | String | 是| 消息内容，不能大于4K|

注: proposal_id和contract_id必须有一个

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="proposal_msg_list"/>[TOP^](#interface)
### <font color=blue>获取投标消息列表</font>
    GET /api/proposal/message

登录: 是

权限：无

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| proposal_id | Int | 是 | 投标ID |
|pagesize|Int|否|默认20条|
|pagenum|Int|否|默认第1页|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
|messages|Array|消息列表|


<div id="notify_list"/>[TOP^](#interface)
### <font color=blue>消息列表</font>
    GET /api/notify

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| rtype | String | 是 | 消息类型:<br/>number:获取未读消息总数<br/>read:获取已读消息列表<br/>unread:获取未读消息列表<br/>all:获取全部<br/>|
|pagesize|Int|否|默认10条|
|pagenum|Int|否|默认第1页|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| notify | Array | 消息数组列表 |
| pagenum | Int | 页码 |
| count | Int | 总数 |


<div id="notify_update"/>[TOP^](#interface)
### <font color=blue>消息更新已读</font>
    PUT /api/notify

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| notify_id | Int | 是 | 消息ID |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="notify_delete"/>[TOP^](#interface)
### <font color=blue>消息删除</font>
    DELETE /api/notify

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| notify_id | Int | 是 | 消息ID |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="freelancer_contract"/>[TOP^](#interface)
### <font color=blue>开发者工作经历查询</font>
    GET /api/freelancers/contract

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| user_id | Int | 是 | 开发者UUID |
| pagesize | Int| 否|默认10条|
| pagenum| Int|否|默认第1页|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| count | Int | 全部数量 |
| pagenum | Int | 页码 |
| contracts | Array | contracts数组|


<div id="my_jobs_list"/>[TOP^](#interface)
### <font color=blue>获取我的工作列表</font>
    GET /api/jobs/my

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| t | String | 否 | 类型,basic获取id和name |
| status | String | 否 | 项目状态,跟参数t不共用<br/>draft:草稿<br/>normal:公开（正常和私有）<br/>close:关闭<br/>delete:删除<br/>all:查询全部|
| pagesize | Int| 否|默认20条,跟参数t不共用|
| pagenum| Int|否|默认第1页,跟参数t不共用|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| jobs | Array | 工作列表 |
| count | Int | 全部数量 |
| pagenum | Int | 页码 |


<div id="freelancer_recommend"/>[TOP^](#interface)
### <font color=blue>为开发者推荐开发者</font>
    GET /api/freelancers/recommend

登录: 是
权限：开发者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| freelancers | Array | 自由职业者列表 |

<div id="get_jump_code"/>[TOP^](#interface)
### <font color=blue>获取登录跳转码</font>
    POST /api/user/jumpcode

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| code | String | 跳转码 |

<div id="jump_code_jump"/>[TOP^](#interface)
### <font color=blue>登录跳转</font>
    GET /jump

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|code|String|是|跳转码|
|path|String|否|跳转路径,如/jobs/new|

注：需要打开浏览器,如果跳转码错误会跳转到首页

<div id="get_friends_list"/>[TOP^](#interface)
### <font color=blue>获取好友列表</font>
    GET /api/friends

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| friends | Array | 好友列表 |

<div id="get_friends_user_info"/>[TOP^](#interface)
### <font color=blue>获取好友信息</font>
    GET /api/friends/users

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|user_ids|String|是|user_id,以逗号分隔，如1,2,3|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| users | Array | 用户信息列表 |


<div id="new_feedback"/>[TOP^](#interface)
### <font color=blue>提交反馈</font>
    POST /api/feedback

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|t |String|是|反馈类型,网站使用suggest<br/>suggest:意见或建议<br/>signin_slow:登录缓慢<br/>run_slow:运行缓慢<br/>message_slow:发送消息缓慢<br/>unusual:异常情况<br/>exit:意外退出|
|score|Int|否|评分1-10,或大于10或小于0会认为是0|
|content|String|是|反馈内容|
|contract|String|否|联系方式|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="contract_evaluate"/>[TOP^](#interface)
### <font color=blue>结束合同评价</font>
    POST /api/contract/evaluate

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id |String|是|合同的UUID|
|question_id |String|是|问题id|
|score|Int|是|是否推荐1-10|
|exchange|Int|是|沟通评分1-5|
|punctual|Int|否|守时评分1-5(需求者)|
|cooper|Int|是|合作评分1-5|
|quality|Int|是|质量评分1-5|
|skill|Int|是|技能评分1-5|
|avail|Int|否|可用性评分1-5(开发者)|
|deliver|Int|否|合理设计交付时间评分1-5(开发者)|
|content|String|是|评价内容500个字|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="get_contract_basic"/>[TOP^](#interface)
### <font color=blue>获取合同列表基本信息</font>
    GET /api/contract/basic

登录: 是


| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| pagesize | Int| 否|默认10条|
| pagenum| Int|否|默认第1页|

注：仅返回合同名字和id

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contracts | Array | 合同 |
| count | Int | 合同总数 |
| pagenum | Int | 当前页吗 |


<div id="get_weekstone_time"/>[TOP^](#interface)
### <font color=blue>获取当前工作时长</font>
    GET /api/weekstone/time

登录: 是


| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id |String|是|合同的UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| today | Int | 当天 |
|total_time|Int|总时长|


<div id="get_weekstone_pay"/>[TOP^](#interface)
### <font color=blue>获取付款时薪里程碑</font>
    GET /api/weekstone/pay

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id |String|是|合同的UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| weekstone | Dict| 当前付款里程碑信息|

<div id="weekstone_create"/>[TOP^](#interface)
### <font color=blue>时薪里程碑开启</font>
    POST /api/weekstone/pay

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|是|合同UUID|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID |
| trade_no | String | 支付交易号 ｜


<div id="weekstone_audit"/>[TOP^](#interface)
### <font color=blue>时薪里程碑审核</font>
    PUT /api/weekstone/pay

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|weekstone_id|Int|是|时薪里程碑ID|
|is_agree|String|是|accept:同意<br/>refuse:结束合同<br/>|
|status|String|否|同意选项，当同意时必输<br/>pause:付款保留合同不开启下一周<br/>continue:付款保留合同开启下一周<br/>stop:付款结束合同|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID,开启下一周返回 | 
| trade_no | String | 支付交易号，开启下一周返回 |

<div id="desktop_weekstone_list"/>[TOP^](#interface)
### <font color=blue>桌面端获取时薪合同</font>
    GET /api/d/weekstone

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|contract_id|String|否|合同uuid，不填，查全部|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
|data|Array|时薪合同|


<div id="contract_weekstone_list"/>[TOP^](#interface)
### <font color=blue>工作日志列表</font>
    GET /api/contract/weekstone

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|||||

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contracts | Array | 时薪合同 |


<div id="bonus_create"/>[TOP^](#interface)
### <font color=blue>奖金订单创建</font>
    POST /api/contract/bonus

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|amount|Float|是|转转金额|
|freelancer_id|String|是|开发者UUID|
|contract_id|String|是|相关合同UUID|
|description|String|否|描述|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID |
| trade_no| String| 支付交易序号|


<div id="bonus_pay"/>[TOP^](#interface)
### <font color=blue>奖金支付</font>
    PUT /api/contract/bonus

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|trade_no|String|是|支付交易序号|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="bonus_query"/>[TOP^](#interface)
### <font color=blue>奖金查询</font>
    GET /api/contract/bonus

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|trade_no|String|是|支付交易序号|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| bonus| Dict | 数据字典|


<div id="notify_setting"/>[TOP^](#interface)
### <font color=blue>通知设置</font>
    POST /api/notify/setting

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|mtype|String|是|通知类型|
|is_send|Bool|是|是否发送|
|rate|String|否|day,week,当mtype=recomm_rate时必须，且is_send有值|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |

<div id="get_statis"/>[TOP^](#interface)
### <font color=blue>获取统计数据</font>
    GET /api/stats/statis

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|||||

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
|data|Json|数据|

<div id="job_delete"/>[TOP^](#interface)
### <font color=blue>删除工作</font>
    DELETE /api/jobs

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
|job_id|String|是|job的UUID|

注：只能删除草稿状态的工作，且彻底删除
返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |


<div id="get_pay_order"/>[TOP^](#interface)
### <font color=blue>支付订单查询</font>
    GET /api/order/pay

登录: 是
权限：需求者

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| contract_id | String | 是 | 合同UUID |
| trade_no | String | 是 | 订单号 ｜
| ptype | String | 是 | 订单类型<br/>milestone:固定价格合同<br/>weekstone:时薪合同<br/>bonus:奖金|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract | Dict | 合同信息，字典类型 |
| records | Array | 支付明细 |


<div id="order_payment"/>[TOP^](#interface)
### <font color=blue>支付订单支付</font>
    POST /api/order/pay

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| contract_id | String | 是 | 合同UUID |
| trade_no | String | 是 | 订单号 ｜
| ptype | String | 是 | 订单类型<br/>milestone:固定价格合同<br/>weekstone:时薪合同<br/>bonus:奖金|

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| contract_id | String | 合同UUID |


<div id="category_options"/>[TOP^](#interface)
### <font color=blue>获取分类选项</font>
    GET /api/category/options

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| category_id | Int | 是 | ID |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| options | Json | |

```

{
    msg: "ok",
    error_code: 0,
    options: {
        framework: true,        //是否有框架选项
        api: true,              //是否有api选项
        stage: true,            //是否有当前阶段
        language: true,         //是否有语言选项
        platform: ""            //分两部分，mobile和desktop，mobile只显示ios,android等, desktop显示Windows, Mac, Linux
    }
}
```

<div id="shot_one"/>[TOP^](#interface)
### <font color=blue>截屏记录详情</font>
    GET /api/weekstone/screenshot

登录: 是

| 参数名 | 参数类型 | 是否必输 | 描述 |
|:---:|:---:|:---:|:---:|
| shot_id | Int | 是 | ID |
| contract_id | String | 是 | 合同UUID |

返回

| 参数名 | 参数类型 | 描述 |
|:---:|:---:|:---:|
| error_code | Int | 错误码 |
| msg | String | 错误信息 |
| shot | Dict| 截屏记录详情 |

