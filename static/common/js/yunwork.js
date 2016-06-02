(function() {
  window['YWORK'] = {
    interval: "",
    wait: 60,
    timeClock: function() { //倒计时时间
      $("span[vcode='clock-vcode']").html(YWORK.wait + "秒后重新发送");
      YWORK.wait--;
      if (YWORK.wait == 0) {
        YWORK.wait = 60;
        clearInterval(YWORK.interval);
        $("span[vcode='clock-vcode']").css("color", "#fff");
        $("span[vcode='clock-vcode']").html("重新发送");
      }
    },
    hideErr: function() {
      $("div[name=error]").hide();
    },
    getValue: function(obj) {
      var type = obj[0].type;
      if (type === "radio") { //单选框
        return $.trim(obj.find("[checked]").val());
      } else if (type === "select-one") { //select框
        return $.trim(obj.find("option:selected").val());
      } else if (type === "checkbox") { //复选框
        var val = [];
        obj.each(function() {
          if ($(this).is(":checked")) {
            val.push($(this).val());
          }
        });
        return val.join(",");
      } else {
        return $.trim(obj.val());
      }
    },
    RegEventBlur: function(form) { //注册失去鼠标焦点事件，做动态验证
      isLegal = true;
      form.find("[required]").each(function() {
        $(this).blur(function() {
          var name = $(this).attr("name");
          var value = YWORK.getValue($(this));
          var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
          var errorNode = form.find("div[data-name=" + errorName + "]");
          if (value === "" || typeof(value) === "undefined") {
            isLegal = false;
            var msg = $(this).attr("required-msg");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          } else {
            isLegal = true;
            errorNode.hide();
          }
        })
      });

      form.find("[equal]").each(function() {
        $(this).blur(function() {
          if (!isLegal) return; //上一级验证已经不通过了
          var equal_name = $(this).attr("equal");
          var name = $(this).attr("name");
          var equal_el = form.find("[name=" + equal_name + "]");
          var value1 = YWORK.getValue($(this));
          var value2 = YWORK.getValue(equal_el);
          var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
          var errorNode = form.find("div[data-name=" + errorName + "]");
          if (value1 !== value2) {
            isLegal = false;
            var msg = $(this).attr("equal-msg");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          } else {
            isLegal = true;
            errorNode.hide();
          }
        })
      });

      form.find("[data-regular]").each(function() {
        $(this).blur(function() {
          if (!isLegal) return; //上一级验证已经不通过了
          var name = $(this).attr("name");
          var pattern = eval($(this).attr("data-regular"));
          var value = YWORK.getValue($(this));
          var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
          var errorNode = form.find("div[data-name=" + errorName + "]");
          if (value != "" && !pattern.test(value)) {
            isLegal = false;
            var msg = $(this).attr("data-msg");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          } else {
            isLegal = true;
            errorNode.hide();
          }
        });
      });
    },
    Validator: {
      is_phone: function(text) {
        var pattern = /^1[3|4|5|7|8][\d]{9}$/;
        return pattern.test(text);
      },
      validateForm: function(form) {
        $("div[name=error]").hide();
        var isLegal = true;
        form.find("[required]").each(function() {
          var name = $(this).attr("name");
          var value = YWORK.getValue($(this));
          if (value === "" || typeof(value) === "undefined") {
            isLegal = false;
            var msg = $(this).attr("required-msg");
            var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
            var errorNode = form.find("div[data-name=" + errorName + "]");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          }
        });

        form.find("[data-regular]").each(function() {
          var name = $(this).attr("name");
          var pattern = eval($(this).attr("data-regular"));
          var value = YWORK.getValue($(this));
          if (value != "" && !pattern.test(value)) {
            isLegal = false;
            var msg = $(this).attr("data-msg");
            var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
            var errorNode = form.find("div[data-name=" + errorName + "]");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          }
        });

        form.find("[equal]").each(function() {
          var equal_name = $(this).attr("equal");
          var name = $(this).attr("name");
          var equal_el = form.find("[name=" + equal_name + "]");
          var value1 = YWORK.getValue($(this));
          var value2 = YWORK.getValue(equal_el);
          var errorName = $(this).attr("data-error") ? $(this).attr("data-error") : name;
          var errorNode = form.find("div[data-name=" + errorName + "]");
          if (value1 !== value2) {
            isLegal = false;
            var msg = $(this).attr("equal-msg");
            errorNode.find("span[class='errorMsg']").text(msg);
            errorNode.show();
          } else {
            errorNode.hide();
          }
        });
        return isLegal;
      }
    },
    compare_time: function(start_time, end_time) {
      if (end_time <= start_time) {
        return false;
      } else {
        return true;
      }
    },
    time2year: function(time) {
      var date = new Date(time);
      return parseInt(date.getFullYear());
    },
    time2month: function(time) {
      var date = new Date(time);
      return parseInt(date.getMonth()) + 1;
    },
    AssemblingData: function(data) {
      if (typeof(data) == "object") {
        data._xsrf = Cookies.get("_xsrf");
      } else {
        data = {};
        data._xsrf = Cookies.get("_xsrf");
      }
      return data;
    },
    postJson: function(url, data) {
      data = YWORK.AssemblingData(data);
      return $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: data
      });
    },
    getJson: function(url, data) {
      //data = YWORK.AssemblingData(data);
      return $.ajax({
        url: url + '?timestamp=' + new Date().getTime(),
        type: 'get',
        dataType: 'json',
        data: data
      });
    },
    deleteJson: function(url, data) {
      data = YWORK.AssemblingData(data);
      return $.ajax({
        url: url,
        type: 'DELETE',
        dataType: 'json',
        data: data
      });
    },
    putJson: function(url, data) {
      data = YWORK.AssemblingData(data);
      return $.ajax({
        url: url,
        type: 'PUT',
        dataType: 'json',
        data: data
      });
    },
    /**
     * 操作提示
     * @params {
     * 	type{String} 类型[success,danger]
     * 	title{String} 标题
     * 	content{String} 内容
     * 	cb{Function} 毁掉函数
     * }
     */
    alert: function(type, title, content, cb) {
      var infoIcon = type === 'danger' ? 'glyphicon-info-sign' : 'glyphicon-ok-sign';
      var html = '<div id="div_alert" role="alert" class="alert-transition">' + '<button type="button" class="close alert_close"><span>×</span></button>' + '<span class="glyphicon ' + infoIcon + ' alert-icon-float-left"></span>' + '<strong>' + title + '</strong>' + '<p>' + content + '</p></div>';

      //展示提示
      if ($('#div_alert').length === 0) {
        $('body').append(html);
      }

      //修改显示内容
      $('#div_alert').find('Strong').text(title);
      $('#div_alert').find('p').text(content);
      $('#div_alert').removeClass('alert-danger').removeClass('alert-success').addClass('alert-' + type).show();

      // 关闭提示
      $('.alert_close').on('click', function() {
        $('#div_alert').hide();
      });

      // 3秒隐藏
      setTimeout(function() {
        $('#div_alert').hide();
      }, 3000)

      // 毁掉执行fn
      if (cb) {
        cb();
      }
    },
    /**
     * 格式化账号信心
     * @param val{String}账号信息
     */
    formatAccount: function(val) {
      var account = val;
      if (val.indexOf('@') >= 0) {
        var pas = val.split('@');
        account = pas[0].substring(0, parseInt(pas[0].length / 2)) + '****@' + pas[1];
      } else {
        account = val.substring(0, 3) + '****' + val.substr(7);
      }
      return account;
    },
    /**
     * 格式化账号信心
     * @param val{String}账号信息
     */
    formatBank: function(val) {
      var account = val;
      if (val) {
        if (val.length === 16) {
          var account = val.substring(0, 4) + '********' + val.substr(12);
        } else {
          var account = val.substring(0, 4) + '********' + val.substr(15);
        }
      }
      return account;
    }
  }
}())