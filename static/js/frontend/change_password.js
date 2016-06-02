$.i18n().then(function(data) {
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  new Vue({
    el: "body",
    data: {
      password_old: "",
      password: "",
      disableBtn: false
    },
    ready: function() {
      YWORK.RegEventBlur($("#form-password"));
    },
    created: function() {

    },
    methods: {
      modify_pwd: function(event) {
        if (!YWORK.Validator.validateForm($("#form-password"))) {
          return;
        }
        var that = this;
        this.disableBtn = true;
        Service.get('UserService').change_pwd({
            password_old: that.password_old,
            password: that.password
          })
          .success(function(result) {
            if (result.error_code != 0) {
              YWORK.alert('danger', '错误提示', CODE[result.error_code]);
              that.disableBtn = false;
            } else {
              YWORK.alert('success', '操作提示', '密码修改成功!', function() {
                setTimeout(function() {
                  window.location.href = "/settings";
                }, 2000)
              });
            }
          })
      }
    }
  });
})