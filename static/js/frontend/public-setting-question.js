Vue.config.delimiters = ['{[', ']}'];
$.i18n().then(function(data) {
  window['CODE'] = data.CODE;
  window['COMMONS'] = data.COMMONS;
  new Vue({
    el: "body",
    data: {
      questions: [],
      user_questions: "",
      question_id: "",
      answer: "",
      answer_old: "",
    },
    ready: function() {
      YWORK.RegEventBlur($("#form-question"));
      var that = this;
      Service.get('CommonService').question({
        "qtype": "user"
      }).success(function(result) {
        that.questions = result.questions;
      });
      Service.get('UserService').question().success(function(result) {
        if (result.error_code == 0) {
          that.user_questions = result.questions[0].name;
        }
      });
    },
    methods: {
      save_user_question: function() {
        if (!YWORK.Validator.validateForm($("#form-question"))) {
          return;
        }
        var that = this;
        Service.get('UserService').post_question({
          question_id: that.question_id,
          answer: that.answer
        }).success(function(result) {
          if (result.error_code != 0) {
            that.showAlert('danger', '错误提示', result.msg);
          } else {
            window.location.href = "/settings";
          }
        });
      },
      update_user_question: function() {
        if (!YWORK.Validator.validateForm($("#form-question"))) {
          return;
        }
        var that = this;
        Service.get('UserService').put_question({
          question_id: that.question_id,
          answer: that.answer,
          answer_old: that.answer_old
        }).success(function(result) {
          if (result.error_code != 0) {
            if (result.msg === 'error answer') {
              that.showAlert('danger', '错误提示', '当前密保回答错误，请再试一次！');
            } else {
              that.showAlert('danger', '错误提示', result.msg);
            }
          } else {
            that.showAlert('success', '操作提示', '密保问题修改成功!', '/settings');
          }
        });
      },
      showAlert: function(type, title, content, url) {
        if (url) {
          YWORK.alert(type, title, content, function() {
            setTimeout(function() {
              window.location.href = url;
            }, 2000);
          })
        } else {
          YWORK.alert(type, title, content);
        }
      }
    }
  })
});