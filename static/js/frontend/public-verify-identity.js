var ve = new Vue({
  el: "#layout",
  data: {},
  ready: function() {
    var that = this;
    $.i18n().then(function(data) {
      window['CODE'] = data.CODE;
      window['COMMONS'] = data.COMMONS;
      YWORK.RegEventBlur($("#form-verify"));
    });
  },
  created: function() {},
  methods: {
    verify: function(event) {
      if (!YWORK.Validator.validateForm($("#form-verify"))) {
        return;
      }
      event.preventDefault();
      $.ajax({
        type: "POST",
        url: "/api/user/verify",
        dataType: "json",
        data: {
          "name": $('input[name=real-name]').val(),
          "id_number": $('input[name=id-number]').val(),
          "_xsrf": Cookies.get("_xsrf")
        },
        success: function(json) {
          if (json.error_code == 0) {
            window.location.href = "/freelancers/settings/identity"
          } else {
            YWORK.alert('danger', '错误提示', CODE[result.error_code]);
          }
        }
      });
    }
  }
});