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
  methods: {
    change_password: function(event){
      var flag = true;
      for(var x in validict){
        if(validict[x](this) == false){
          flag = false;
        }
      }
      if(!flag){
        return;
      }
      var that = this;
      $.ajax({
        type: "post",
        url: "/api/password/reset",
        cache: false,
        dataType: "json",
        data: {
          username: that.username,
          password: that.password1,
          _xsrf: Cookies.get("_xsrf"),
          vcode: that.vcode
        },
        error: function(xhr, textStatus){
        },
        success: function(result){
          if(result.error_code != 0){
            that.errRes = result.msg;
          }else{
            alert("ok")
          }
        }
      });
    },
    send_code: function(event){
      var v = validict.username(this);
      console.log(v);
      if(!v){
        return
      }
      var that = this;
      $.ajax({
        type: "post",
        url: "/api/verifycode",
        cache: false,
        dataType: "json",
        data: {
          phone: that.username,
          _xsrf: Cookies.get("_xsrf"),
          register: true
        },
        error: function (xhr, textStatus) {
        },
        success: function (result) {
          if(result.error_code != 0){
            that.errRes = result.msg;
          }else{
            that.disVcode = true;
            timer(20, that);
          }
        }
      });
    },
    validate: function(item, event) {
      validict[item](this);
    },
  }
});

var validict = {
  "username": function(fp){
    var reg_name = /^[a-zA-z]\w{3,19}$/;
    var reg_phone = /^1\d{10}$/;
    var reg_email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(reg_name.test(fp.username) || reg_phone.test(fp.username) || reg_email.test(fp.username)){
      fp.errUsername = "";
      return true;
    }else{
      fp.errUsername = "用户名不合法";
      return false;
    }
  },
  "vcode": function(fp){
    var reg_vcode = /^\d{6}$/;
    if(!reg_vcode.test(fp.vcode)){
      fp.errVcode = "验证码不合法";
      return false;
    }else{
      fp.errVcode = "";
    }
  },
  "password1": function(fp){
    if(fp.password1.length < 6 || fp.password1.length > 20){
      fp.errPassword1 = "密码长度为6-20位";
      return false;
    }else{
      fp.errPassword1 = "";
    }
  },
  "password2": function(fp){
    if(fp.password2.length < 6 || fp.password2.length > 20){
      fp.errPassword2 = "密码长度为6-20位";
      return false;
    }else{
      fp.errPassword2 = "";
    }

    if(fp.password != fp.passwordTwo){
      fp.errPassword2 = "两次密码不一致";
      return false;
    }else{
      fp.errpassword2 = "";
    }
  }
};


function timer(num, that) {
  var counter = setInterval(function(){
    that.txtVcode = "已发送(" + num + ")";
    num = num -1;
    if(num <= 0){
      that.disVcode = false;
      that.txtVcode = "获取验证码";
      clearInterval(counter);
      return;
    }
  }, 1000);
}
