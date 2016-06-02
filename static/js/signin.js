Vue.config.delimiters = ['{[', ']}'];

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
    $.i18n();
  },
  //事件
  methods: {    
    validate: function(item, event) {
      validict[item](this);
    },
    login:function(event){
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
        url: '/api/user/signin',
        type: 'post',
        dataType: 'json',
        data: {
          username: that.username.trim(),
          password: that.password.trim(),
          _xsrf: Cookies.get("_xsrf"),
          remember: that.remember
        },
        success: function(result){
          if(result.error_code != 0){
            that.errRes = CODE[result.error_code];
            alert(this.errRes);
          }
          else{
            $("#success").show();
            var next = $.getParameterByName("next");
            if(next){
              location.href = next;
            }else{
              location.href = "/";
            }
          }
        }
      });
    }
  }
});

var validict = {
    "username": function(fr) {
      var reg_name = /^[a-zA-z]\w{3,19}$/;
      var reg_phone = /^1\d{10}$/;
      var reg_email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
      if(reg_name.test(fr.username) || reg_phone.test(fr.username) || reg_email.test(fr.username)){
        fr.errUsername = "";
        return true;
      }else{
        fr.errUsername = "用户名不合法";
        return false;
      }
  },
  "password": function(fr) {
    if(fr.password == ""){
      fr.errPassword = "此字段不能为空";
      return false;
    }else if(fr.password.length < 6 || fr.password.length > 20){
      fr.errPassword = "密码长度为6-20位";
      return false;
    }else{
      fr.errPassword = "";
    }
  }
};

