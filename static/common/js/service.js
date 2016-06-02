
var Service = {
	services :[],//服务容器
	modules:[],
	factory:function(name,func){
		//服务存在 直接返回
		if(this.services.hasOwnProperty(name)){
			return;
		}
		this.services[name] = func();
	},
	get : function(name){
		return this.services[name];
	},
	load:function(module){
		var name = module;
		module = eval(module);
		this.modules[name] = module();
		return 	this.modules[name];
	},
	getModule:function(module){
			return this.modules[module];
	}
};

Service.factory("CommonService",function(){
	return {
		verifycode:function(data){
			return YWORK.postJson("/api/verifycode",data,'application/json')
		},
		address:function(data){
			return YWORK.getJson("/api/address",data,'application/json')
		},
		category:function(data){
			return YWORK.postJson("/api/category",data,'application/json')
		},
		question:function(data){
			return YWORK.getJson("/api/question",data,'application/json')
		}
	}
});

//授权服务接口定义
Service.factory('AuthService', function(){
	return {
		login:function(data){
			return YWORK.postJson("/api/user/signin",data,'application/json')
		},
		findpwd:function(data){
			return YWORK.postJson("/api/user/password/reset",data,'application/json')
		},
		signup:function(data){
			return YWORK.postJson("/api/user/signup",data,'application/json')
		}
	}
});

//简历个人中心服务接口
Service.factory('ResumeService', function(){
	return {
		get_profile:function(data){//获取用户资料信息
			return YWORK.getJson("/api/user/profile",data,'application/json')
		},
		post_resume:function(data){//完善经历
			return YWORK.postJson("/api/user/resume",data,'application/json')
		},
		post_profile:function(data){//创建或者更新用户信息
			return YWORK.postJson("/api/user/profile",data,'application/json')
		},
		post_other_profile:function(data){
			return YWORK.postJson("/api/user/other/create",data,'application/json')
		},
		put_profile:function(data){//或者更新用户信息
			return YWORK.putJson("/api/user/profile",data,'application/json')
		},
		get_employment:function(data){
			return YWORK.getJson("/api/employment",data,'application/json')
		},
		get_education:function(data){
			return YWORK.getJson("/api/education",data,'application/json')
		},
		get_portfolio:function(data){
			return YWORK.getJson("/api/portfolio",data,'application/json')
		},
		post_employment:function(data){
				return YWORK.postJson("/api/employment",data,'application/json')
		},
		post_education:function(data){
				return YWORK.postJson("/api/education",data,'application/json')
		},
		post_project:function(data){
				return YWORK.postJson("/api/portfolio",data,'application/json')
		},
		put_employment:function(data){
				return YWORK.putJson("/api/employment",data,'application/json')
		},
		put_education:function(data){
				return YWORK.putJson("/api/education",data,'application/json')
		},
		put_project:function(data){
				return YWORK.putJson("/api/portfolio",data,'application/json')
		},
		delete_employment:function(data){
				return YWORK.deleteJson("/api/employment",data,'application/json')
		},
		delete_education:function(data){
				return YWORK.deleteJson("/api/education",data,'application/json')
		},
		delete_project:function(data){
				return YWORK.deleteJson("/api/portfolio",data,'application/json')
		},

	}
});

Service.factory('UserCategoryService',function(){
	return {
		get_category:function(data){
			return YWORK.postJson("/api/category",data,'application/json')
		},
		user_category:function(data){
			return YWORK.getJson("/api/user/category",data,'application/json')
		},
		user_category_update:function(data){
			return YWORK.postJson("/api/user/category",data,'application/json')
		}
	}
});

Service.factory('UserService',function(){
	return {
	
		question:function(data){
			return YWORK.getJson("/api/user/question",data,'application/json')
		},
		post_question:function(data){
			return YWORK.postJson("/api/user/question",data,'application/json')
		},
		put_question:function(data){
			return YWORK.putJson("/api/user/question",data,'application/json')
		},
		change_pwd:function(data){
			return YWORK.postJson("/api/user/password/change",data,'application/json')
		},
		account_records:function(data){
            return YWORK.getJson("/api/margin/record",data,'application/json')
        },
		bank_type:function(data){
			return YWORK.getJson("/api/margin/bank",data,'application/json')
		},
		bank_list:function(data){
			return YWORK.getJson("/api/margin/card",data,'application/json')
		},
		save_card:function(data){
			return YWORK.postJson("/api/margin/card",data,'application/json')
		},
		delete_card:function(data){
			return YWORK.deleteJson("/api/margin/card",data,'application/json')
		},
		create_alipay:function(data){
			return YWORK.postJson("/api/user/alipay",data,'application/json')
		},
		delete_alipay:function(data){
			return YWORK.deleteJson("/api/user/alipay",data,'application/json')
		}
	}
});

Service.factory('WorkService',function(){
	return {
		works:function(data){
			return YWORK.postJson("/api/jobs/search",data,'application/json')
		},
		collect:function(data){
				return YWORK.postJson("/api/favorite",data,'application/json')
		},
		del_collect:function(data){
				return YWORK.deleteJson("/api/favorite",data,'application/json')
		},
		collect_list:function(data){
				return YWORK.getJson("/api/favorite",data,'application/json')
		},
		subscribe_works:function(data){
				return YWORK.getJson("/api/subscribe",data,'application/json')
		},
		post_subscribe:function(data){
				return YWORK.postJson("/api/subscribe",data,'application/json')
		},
	}
});

Service.factory('BidService',function(){
	return {
		//招投标
		bid:function(data){
			return YWORK.postJson("/api/proposal",data,'application/json')
		},
		select_bid:function(data){
			return YWORK.getJson("/api/proposal",data,'application/json')
		},
		update_bid:function(data){
			return YWORK.putJson("/api/proposal",data,'application/json')
		},
	}
});

Service.factory('ContractService',function(){
	return {
		select_contract:function(data){
			return YWORK.getJson("/api/contract",data,'application/json')
		},
		update_contract:function(data){
			return YWORK.putJson("/api/contract",data,'application/json')
		},
		team_contract:function(data){
			return YWORK.getJson("/api/user/role",data,'application/json')
		},
		

	}
});
//需求我的项目
Service.factory('Myproject',function(){
	return {
		proposal:function(data){
			return YWORK.getJson("/api/jobs/proposal?t="+ new Date().getTime(),data,'application/json')
		},
		pro_contract:function(data){
			return YWORK.getJson("/api/contract",data,'application/json')
		},
		pro_details:function(data){
			return YWORK.getJson("/api/jobs",data,'application/json')
		},
		update_pro:function(data){
			return YWORK.putJson("/api/jobs",data,'application/json')
		}
	}
});
//付款
Service.factory('Payment',function(){
	return {
		pay_apply:function(data){
			return YWORK.getJson("/api/milestone/pay",data,'application/json')
		},
		agree_pay:function(data){
			return YWORK.putJson("/api/milestone",data,'application/json')
		},
	}
});
//创建需求者账号
Service.factory('client',function(){
	return {
		creat_client:function(data){
			return YWORK.postJson("/api/user/client",data,'application/json')
		},
		search_freelancer:function(data){
			return YWORK.getJson("/api/freelancers/search",data,'application/json')
		},
		role_team:function(data){
			return YWORK.getJson("/api/user/role",data,'application/json')
		},
		freelancers_list:function(data){
			return YWORK.getJson("/api/client/freelancers",data,'application/json')
		}
	}
});
//更多的模块服务
Service.factory('accountService',function(){
	return {
		get_account_basic:function(data){
			return YWORK.getJson('/api/margin/basic', data, 'application/json')
		}
	}
});
//消息提醒模块
Service.factory('notify',function(){
	return {
		get_notify:function(data){
			return YWORK.getJson('/api/notify', data, 'application/json')
		},
		put_notify:function(data){
			return YWORK.putJson('/api/notify', data, 'application/json')
		},
		delete_notify:function(data){
			return YWORK.deleteJson('/api/notify', data, 'application/json')
		}
	}
});
