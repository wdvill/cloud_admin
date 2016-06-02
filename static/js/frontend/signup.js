Vue.config.delimiters = ['{[', ']}'];

$.i18n().then(function(data) {
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;

  var sendvcode = function(vue_obj) {
    var that = vue_obj;
    if (YWORK.wait < 60) { //一分钟不满
      return;
    }
    YWORK.hideErr();
    if ($.trim(that.phone) === "") {
      $("div[data-name=phone]").find("span[class=errorMsg]").text("手机号码必填");
      $("div[data-name=phone]").show();
      return;
    }
    if (!YWORK.Validator.is_phone($.trim(that.phone))) {
      $("div[data-name=phone]").find("span[class=errorMsg]").text("手机号码格式错误");
      $("div[data-name=phone]").show();
      return;
    }
    Service.get('CommonService').verifycode({
      vtype: "register",
      phone: that.phone,
      _xsrf: Cookies.get("_xsrf"),
    }).success(function(result) {
      if (result.error_code != 0) {
        that.remoteErr = CODE[result.error_code];
      } else {
        YWORK.interval = setInterval(YWORK.timeClock, 1000);
        that.realVcode = result.vcode
      }
    })
  }

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
      realVcode: '',
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
    ready: function() {
      var that = this;
      YWORK.RegEventBlur($("#form-sign-free"));
    },
    methods: {
      sendvcode: function(event) {
        sendvcode(this);
      },
      register: function(event) {
        if (!YWORK.Validator.validateForm($("#form-sign-free"))) {
          return;
        }
        var that = this;
        if (this.realVcode != this.vcode) {
          $('.error-div[data-name="vcode"]').show()
          $('.error-div[data-name="vcode"]').find('.errorMsg').html('验证码不正确')
          return;
        } else {
          $('.error-div[data-name="vcode"]').hide()
        }
        Service.get('AuthService').signup({
          name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          rtype: 1,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          username: that.username
        }).success(function(result) {
          if (result.error_code != 0) {
            that.remoteErr = CODE[result.error_code];
          } else {
            that.remoteErr = "注册成功";
            location.href = "/users/guide";
          }
        })
      },
    }
  });


  var company = new Vue({
    el: "#home2",
    data: {
      name: "",
      phone: "",
      acceptSms: true,
      legal: true,
      password: "",
      vcode: "",
      realVcode: '',
      company: "",
      disVcode: false,
      remoteErr: false,

      errName: "",
      errPhone: "",
      errPassword: "",
      errVcode: "",
      errCompany: ""
    },
    ready: function() {
      $.i18n();
      YWORK.RegEventBlur($("#form-company"));
    },
    methods: {
      sendvcode: function(event) {
        sendvcode(this);
      },
      register: function(event) {
        if (!YWORK.Validator.validateForm($("#form-company"))) {
          return;
        }
        var that = this;
        if (this.realVcode != this.vcode) {
          $('.error-div[data-name="vcode"]').show()
          $('.error-div[data-name="vcode"]').find('.errorMsg').html('验证码不正确')
          return;
        } else {
          $('.error-div[data-name="vcode"]').hide()
        }
        var data = {
          name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          username: that.phone,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          cname: that.company,
          rtype: 2
        }
        Service.get('AuthService').signup(data)
          .success(function(json) {
            if (json.error_code != 0) {
              that.remoteErr = CODE[json.error_code];
            } else {
              that.remoteErr = "注册成功";
              if (data.rtype == 1) {
                location.href = "/users/guide";
              } else {
                location.href = "/clients/guide";
              }
            }
          })
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
      realVcode: '',
      txtVcode: "获取验证码",
      disVcode: false,
      remoteErr: false,

      errName: "",
      errPhone: "",
      errPassword: "",
      errVcode: ""
    },
    ready: function() {
      YWORK.RegEventBlur($("#form-person"));
    },
    methods: {
      sendvcode: function(event) {
        sendvcode(this);
      },
      register: function(event) {
        if (!YWORK.Validator.validateForm($("#form-person"))) {
          return;
        }
        var that = this;
        if (this.realVcode != this.vcode) {
          $('.error-div[data-name="vcode"]').show()
          $('.error-div[data-name="vcode"]').find('.errorMsg').html('验证码不正确')
          return;
        } else {
          $('.error-div[data-name="vcode"]').hide()
        }
        var data = {
          name: that.name,
          phone: that.phone,
          password: that.password,
          vcode: that.vcode,
          username: that.phone,
          notice: that.acceptSms,
          _xsrf: Cookies.get("_xsrf"),
          rtype: 3
        }
        Service.get('AuthService').signup(data)
          .success(function(json) {
            if (json.error_code != 0) {
              that.remoteErr = CODE[json.error_code];
            } else {
              that.remoteErr = "注册成功";
              if (data.rtype == 1) {
                location.href = "/users/guide";
              } else {
                location.href = "/clients/guide";
              }
            }
          })
      }
    }
  });
});