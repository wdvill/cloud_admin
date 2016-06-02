Vue.config.delimiters = ['{[', ']}'];

var freelancer = new Vue({
  el: "#form-sign-free",
  data: {
    name: "",
    phone: "",
    acceptSms: true,
    legal: true,
    password: "",
    passwordTwo: "",
    vcode: "",
    username: "",
    txtVcode: "获取验证码",
    disVcode: false,
    remoteErr: false,

    errName: "",
    errPhone: "",
    errPassword: "",
    errUsername: "",
    errVcode: "",
    errPasswordTwo: ""
  },
  created: function(){
    $.i18n();
  },
  methods: {
    sendvcode: function(event) {
      sendvcode(this);
    },
    register: function(event) {
      //this.name = fr.name.trim();
      //this.phone = fr.phone.trim();
      //this.password = fr.password.trim();
      //this.passwordTwo = fr.passwordTwo.trim();
      //this.username = fr.username.trim();
      //this.vcode = fr.vcode.trim();
      var that = this;
      var flag = true;
      for(var x in validict){
        if(validict[x](this) == false){
          flag = false;
        }
      }
      if(!flag){
        return;
      }
      that.remoteErr = "";
      $.ajax({
        type: "post",
        url: "/api/user/signup",
        cache: false,
        dataType: "json",
        data: {
          name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          rtype: 1,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          username: that.username
        },
        error: function (xhr, textStatus) {
        },
        success: function (json) {
          if(json.error_code != 0){
            that.remoteErr = CODE[json.error_code];
          }else{
            that.remoteErr = "注册成功";
            location.href="/users/guide";
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
  "name": function(fr) {
    var reg = /^[\u4e00-\u9fa5]/;
    if(!reg.test(fr.name)){
      fr.errName = "姓名必须为汉字";
      return false;
    }else{
      fr.errName = "";
    }
  },
  "phone": function(fr) {
    var reg1 = /^1\d{10}$/;
    if(!reg1.test(fr.phone)){
      fr.errPhone = "手机号须为11位数字";
      return false;
    }else{
      fr.errPhone = "";
    }
  },
  "username": function(fr) {
    if(!fr.hasOwnProperty("username")){
      return;
    }
    var reg2 = /[a-zA-Z_]{4,20}/;
    if(!reg2.test(fr.username)){
      fr.errUsername = "昵称只能为4-20位大小写字母加下划线组合";
      return false;
    }else{
      fr.errUsername = "";
    }
  },
  "password": function(fr) {
    if(fr.password.length < 6 || fr.password.length > 20){
      fr.errPassword = "密码长度为6-20位";
      return false;
    }else{
      fr.errPassword = "";
    }
  },
  "passwordTwo": function(fr) {
    if(!fr.hasOwnProperty("passwordTwo")){
      return;
    }
    if(fr.password != fr.passwordTwo){
      fr.errPasswordTwo = "两次密码不一致";
      return false;
    }else{
      fr.errpasswordTwo = "";
    }
  },
  "vcode": function(fr) {
    var reg3 = new RegExp("^[0-9]*$");
    if(fr.vcode == ""){
      fr.errVcode = "此字段为必填项";
      return false;
    }
    if(!reg3.test(fr.vcode)){
      fr.errVcode = "验证码为数字";
      return false;
    }else{
      fr.errVcode = "";
    }
  },
  "legal": function(fr) {
    if(!fr.legal){
      $('#error').modal('show');
      return false;
    }
  },
  "company": function(fr) {
    if(!fr.hasOwnProperty("company")){
      return;
    }
    if(fr.company.length < 2 || fr.company.length > 150){
      fr.errCompany = "公司名称为2-150位";
      return false;
    }else{
      fr.errCompany = "";
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

function sendvcode(that) {
  var reg1 = /[0-9]{11,11}/;
  if(!reg1.test(that.phone)){
    that.errPhone = "手机号须为11位数字";
    return;
  }else{
    that.errPhone = "";
  }
  that.remoteErr = "";
  $.ajax({
    type: "post",
    url: "/api/verifycode",
    cache: false,
    dataType: "json",
    data: {
      _xsrf: Cookies.get("_xsrf"),
      phone: that.phone
    },
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code != 0){
        that.remoteErr = CODE[json.error_code];
      }else{
        that.disVcode = true;
        timer(20, that);
      }
    }
  });
}

function register(that, data) {
  var flag = true;
  for(var x in validict){
    if(validict[x](that) == false){
      console.log(x);
      flag = false;
    }
  }
  if(!flag){
    return;
  }
  that.remoteErr = "";
  $.ajax({
    type: "post",
    url: "/api/user/signup",
    cache: false,
    dataType: "json",
    data: data,
    error: function (xhr, textStatus) {
    },
    success: function (json) {
      if(json.error_code != 0){
        that.remoteErr = CODE[json.error_code];
      }else{
        that.remoteErr = "注册成功";
        if(data.rtype == 1){
          location.href="/users/guide";
        }else{
          location.href="/jobs/new";
        }
      }
    }
  });
}

var company = new Vue({
  el: "#home2",
  data: {
    name: "",
    phone: "",
    acceptSms: true,
    legal: true,
    password: "",
    vcode: "",
    company: "",
    txtVcode: "获取验证码",
    disVcode: false,
    remoteErr: false,

    errName: "",
    errPhone: "",
    errPassword: "",
    errVcode: "",
    errCompany: ""
  },
  ready: function(){
    $.i18n();
  },
  methods: {
    sendvcode: function(event) {
      sendvcode(this);
    },
    register: function(event) {
      var that = this;
      var data = {name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          username: that.phone,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          cname: that.company,
          rtype: 2}
      register(this, data);
    },
    validate: function(item, event) {
      validict[item](this);
    }
  }
});

var person = new Vue({
  el: "#profile2",
  data: {
    name: "",
    phone: "",
    acceptSms: true,
    legal: true,
    password: "",
    vcode: "",
    txtVcode: "获取验证码",
    disVcode: false,
    remoteErr: false,

    errName: "",
    errPhone: "",
    errPassword: "",
    errVcode: ""
  },
  methods: {
    sendvcode: function(event) {
      sendvcode(this);
    },
    register: function(event) {
      var that = this;
      var data = {name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          username: that.phone,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          rtype: 3
      }
      register(this, data);
    },
    validate: function(item, event) {
      validict[item](this);
    }
  }
});
