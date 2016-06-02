var selectize = null;
var Profile = function() {
  return new Vue({
    el: "#body",
    data: {
      globel: {},
      profile: {},
      other_languages: [],
      x: "",
      y: "",
      w: "",
      h: "",
      language_level: "",
      errLanguagesMsg: "其他语言不为空",
      languages: [],
      del_index: 0
    },
    created: function() {
      var arr = $("#ipt-skills").val().split(",");
      var arr1 = [];
      for (var i = 0; i < arr.length; i++) {
        arr1.push({
          value: arr[i],
          text: arr[i]
        });
      }
      var $select = $('#select-skills').selectize({
        plugins: ['remove_button'],
        delimiter: ',',
        persist: false,
        maxItems: null,
        options: arr1,
        create: false
      });
      selectize = $select[0].selectize;
    },

    ready: function() {
      var that = this;
      YWORK.RegEventBlur($("#form-profile"));
      Service.get('ResumeService').get_profile().success(function(result) {
        if (result.error_code == 0) {
          that.profile = {}
          that.other_languages = [];
          that.profile = result.profile;
          that.profile.skills = result.profile.skills.join(",");
          selectize.setValue(result.profile.skills.split(','))
          for (var i = 0; i < result.profile.languages.length; i++) {
            that.other_languages.push({
              name: result.profile.languages[i].name,
              level: result.profile.languages[i].level,
            })
          }
        }
        that.globel = COMMONS;
      })
    },
    watch : {
      'profile.skills': function() {
        if (this.profile.skills != '') {
          $('.error-div[data-name="skills"]').hide()
          $('.error-div[data-name="skills"]').find('.errorMsg').html('')
        } else {
          $('.error-div[data-name="skills"]').show()
          $('.error-div[data-name="skills"]').find('.errorMsg').html('技能必选')
        }
      }
    },
    methods: {
      save_go_on: function() { //提交个人信息
        if (!YWORK.Validator.validateForm($("#form-profile"))) {
          return;
        }
        var that = this;
        // if(that.other_languages.length <= 0){//其他语言非选择的
        // 		that.errLanguages = true;
        // 		return ;
        // }
        var other = {};
        for (var i = 0; i < that.other_languages.length; i++) {
          other[that.other_languages[i].name] = that.other_languages[i].level;
        }
        var data = {
          title: that.profile.title,
          intro: that.profile.overview,
          email: that.profile.email,
          workload: that.profile.workload,
          english: that.profile.english,
          skills: that.profile.skills,
          other: JSON.stringify(other),
        }
        Service.get('ResumeService').post_profile(data).success(function(result) {
          if (result.error_code == 0) {
            window.location.href = "/users/profile/step/3";
          }
        });
      },
      upload_avatar: function() {
        var that = this;
        if (!that.x || that.x == "") {
          alert("请选择图片");
          return;
        }
        var formData = new FormData();
        var f = $("#photo")[0].files[0];
        if (!f) {
          alert("请选择图片");
          return;
        }
        formData.append('file', f);
        var params = "x=" + that.x + "&y=" + that.y + "&w=" + that.w + "&h=" + that.h;
        params += "&_xsrf=" + Cookies.get("_xsrf") + "&boundx=" + boundx + "&boundy=" + boundy;
        $.ajax({
          url: '/api/attachment?t=avatar&' + params,
          type: 'POST',
          cache: false,
          data: formData,
          processData: false,
          contentType: false,

          error: function(xhr, textStatus) {},
          success: function(json) {
            json = $.parseJSON(json);
            if (json.error_code > 0) {
              alert(CODE[json.error_code]);
              return;
            }
            that.profile.avatar = json.avatar;
            $("#photo_view").attr("src", json.avatar);
            $("#btn-closeM").click();
          }
        });
      },
      prev_category: function() {
        window.location.href = "/users/profile/step/1"
      }
    }
  });
}