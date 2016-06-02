Vue.config.delimiters = ['{[', ']}'];

var forgetpassword = new Vue({
  el: "#form-password-forget",
  data: {
    username: "",
    vcode: "",
    password1: "",
    password2: "",

    errRes: "",
    txtVcode: "获取验证码",
    disVcode: false,
    errUsername: "",
    errVcode: "",
    errPassword1: "",
    errPassword2: ""
  },
  ready: function() {
    YWORK.RegEventBlur($("#form-password-forget"));
  },
  methods: {
    change_password: function(event){
      if(!YWORK.Validator.validateForm($("#form-password-forget"))){
    		return ;
      }
      var that = this;
      Service.get('AuthService').findpwd({
          username: that.username,
          password: that.password1,
          _xsrf: Cookies.get("_xsrf"),
          vcode: that.vcode
        }).success(function(result){
        	if(result.error_code != 0){
                that.errRes = result.msg;
              }else{
		            window.location.href="/forgotpassword/success";
              }
        });
    },
    send_code: function(event){
      var that = this;
      if(YWORK.wait < 60){//一分钟不满
  		 return ;
  	  }
      YWORK.hideErr();
      if($.trim(that.username) === ""){
    	  $("div[data-name=username]").find("span[class=errorMsg]").text("手机号码必填");
    	  $("div[data-name=username]").show();
    	  return ;
      }
      if(!YWORK.Validator.is_phone($.trim(that.username))){
    	  $("div[data-name=username]").find("span[class=errorMsg]").text("手机号码格式错误");
    	  $("div[data-name=username]").show();
    	  return ;
      }
      Service.get('CommonService').verifycode({
        vtype: "forget",
        phone: that.username,
        _xsrf: Cookies.get("_xsrf")
      }).success(function(result){
        console.log(result.error_code);
        if(result.error_code != 0){
          that.errRes = result.msg;
        }else{
          YWORK.interval = setInterval(YWORK.timeClock,1000);
        }
      })
    },
  }
});
