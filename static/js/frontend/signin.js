Vue.config.delimiters = ['{[', ']}'];
$.i18n().then(function(data){
    window['CODE'] = data.CODE;
    window['COMMONS'] = data.COMMONS;
	var formSignin = new Vue({
	  el: "#form-signin",
	  data: {
	    username: "",
	    password: "",
	    remember: false,
	
	    errRes: "",
	    errUsername: "",
	    errPassword: ""
	  },
	  ready: function() {
	   
	    YWORK.RegEventBlur($("#form-signin"));
	  },
	  //事件
	  methods: {
	    login:function(event){
	    	if(!YWORK.Validator.validateForm($("#form-signin"))){
	    		return ;
	    	}
	      var that = this;
	    	Service.get('AuthService').login({
	            username: that.username.trim(),
	            password: that.password.trim(),
	            _xsrf: Cookies.get("_xsrf"),
	            remember: that.remember
	          }).success(function(result){
	        	  if(result.error_code != 0){
	                  that.errRes = CODE[result.error_code];
	              }else{
	                  $("#success").show();
	                  var next = $.getParameterByName("next");
	                  if(next){
	                    location.href = next;
	                  }else{
	                    location.href = "/";
	                  }
	              }
	          });
	    }
	  }
	});
});
