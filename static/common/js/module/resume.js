var Resume = function () {
  return new Vue({
    el: "#profile_edit",
    data: {
      profile: {},
      other_languages: [],
      other_language: "",
      language_level: "",
      employments: [], //工作经历列表
      educations: [], //教育经历
      portfolios: [], //项目经验
      prarent_address: [], //地址列表china    Service.get('CommonService')
      child_address: [], //
      role_list: {
        "Intern": 1,
        "General staff": 2,
        "Charger": 3,
        "Manager": 4,
        "General manager": 5,
        "Founder": 6
      },
      role_list_map: [],
      category_list_map: [],
      child_category: [],
      employment: {},
      address_id: "",
      address_pid: "",
      category_pid: "",
      education: {},
      education_start_year: '',
      education_end_year: '',
      project: {},
      level: "",
      item: {},
      index: "",
      type: "",
      globel: {},
      picture: {},
      hourly: "",
      overview: "",
      errRes: "",
      dateErr: ''
    },
    computed: {
      // 一个计算属性的 getter
      actual_amount: function () {
        // `this` 指向 vm 实例
        return (this.hourly * 0.9).toFixed(2);
      }
    },
    ready: function () {
      var that = this;
      that.globel = COMMONS;
      YWORK.RegEventBlur($("#employment-form"));
      YWORK.RegEventBlur($("#education-form"));
      YWORK.RegEventBlur($("#project-form"));
      Service.get('CommonService').address({
        address_id: 1
      }).success(function (result) {
        that.prarent_address = result.addresses;

      });
      Service.get('CommonService').category({
        category_id: 0
      }).success(function (result) {
        that.category_list_map = result.categorys;
      });

      Service.get('ResumeService').get_profile().success(function (result) {
        that.profile = result.profile;
        for (var i = 0; i < that.profile.languages.length; i++) {
          that.other_languages.push({
            name: result.profile.languages[i].name,
            level: result.profile.languages[i].level,
          })
        }
        that.level = result.profile.level;
        that.hourly = result.profile.hourly;
      });

      Service.get('ResumeService').get_employment().success(function (result) {
        that.employments = result.employments;
        that.globel = COMMONS;
      });

      Service.get('ResumeService').get_education().success(function (result) {
        that.educations = result.educations;
        that.globel = COMMONS;
      });

      Service.get('ResumeService').get_portfolio().success(function (result) {
        that.portfolios = result.portfolios;
        that.globel = COMMONS;
      });

    },
    methods: {
      select_child_address: function () {
        var that = this;
        Service.get('CommonService').address({
          address_id: that.address_pid
        }).success(function (result) {
          that.child_address = result.addresses;
        })
      },
      select_child_category: function () {
        var that = this;
        Service.get('CommonService').category({
          category_id: that.category_pid
        }).success(function (result) {
          that.child_category = result.categorys;
        })
      },
      save_employment: function (type) { //保存工作经历
        YWORK.hideErr();
        if (!YWORK.Validator.validateForm($("#employment-form"))) {
          return;
        }
        // 开始日期不能大于结束日期
        if (!this.compareTime()) {
          return
        }
        if (this.employment_start_month < 10) {
          this.employment_start_month = "0" + this.employment_start_month;
        }
        if (this.employment_end_month < 10) {
          this.employment_end_month = "0" + this.employment_end_month;
        }

        var start_at = this.employment_start_year + "-" + this.employment_start_month;
        var end_at = this.employment_end_year + "-" + this.employment_end_month;
        var that = this;
        var data = {
          start_at: start_at,
          end_at: end_at,
          company: that.employment.company,
          city_id: that.address_id,
          title: that.employment.title,
          role: that.employment.role,
          working: that.employment.working ? true : false,
          detail: that.employment.detail
        }
        if (!that.employment.id) {
          Service.get('ResumeService').post_employment(data).success(function (result) {
            if (result.error_code == 0) {
              Service.get('ResumeService').get_employment().success(function (result) {
                that.employments = result.employments;
                if (!type) {
                  $(".modal01").modal('hide');
                } else {
                  that.employment = {};
                }
              })
            }
          })
        } else {
          data.eid = that.employment.id;
          Service.get('ResumeService').put_employment(data).success(function (result) {
            if (result.error_code == 0) {
              Service.get('ResumeService').get_employment().success(function (result) {
                that.employments = result.employments;
                if (!type) {
                  $(".modal01").modal('hide');
                } else {
                  that.employment = {};
                }
              })
            }
          })
        }
      },
      edit_employment: function (item) { //编辑工作经历
        // 开始日期不能大于结束日期
        if (!this.compareTime()) {
          return
        }
        YWORK.hideErr();
        var that = this;
        this.employment = item;
        this.$set('employment_start_year', YWORK.time2year(item.start_at));
        this.$set('employment_end_year', YWORK.time2year(item.end_at));
        this.employment_start_month = YWORK.time2month(item.start_at);
        this.employment_end_month = YWORK.time2month(item.end_at);
        this.address_pid = item.city.parent_id;
        this.address_id = item.city.id;
        Service.get('CommonService').address({
          address_id: item.city.parent_id
        }).success(function (result) {
          that.child_address = result.addresses;
        })
        $(".modal01").modal('show');
      },
      /* 比较开始时间和结束时间 */
      compareTime() {
        var start_at = (new Date(this.employment_start_year + '-' + this.employment_start_month + '-01')).getTime()
        var end_at = (new Date(this.employment_end_year + '-' + this.employment_end_month + '-01')).getTime()
        var now = (new Date()).getTime()
        this.dateErr = ''
          // 开始日期不能大于结束日期
        if (!this.employment.working && start_at > end_at) {
          this.dateErr = '开始日期不能大于结束日期'
          return false
        }
        // 开始日期不能大于当前日期
        if (start_at > now) {
          this.dateErr = '开始日期不能大于当前日期'
          return false
        }
        // 结束日期不能大于当前日期
        if (!this.employment.working && end_at > now) {
          this.dateErr = '结束日期不能大于当前日期'
          return false
        }
        return true
      },
      save_education: function (type) {

        YWORK.hideErr();
        if (!YWORK.Validator.validateForm($("#education-form"))) {
          return;
        }
        var start_at = this.education_start_year;
        var end_at = this.education_end_year;
        if (!YWORK.compare_time(start_at, end_at)) {
          var errorNode = $("#education-form").find("div[data-name=datetime]");
          errorNode.find(".errorMsg").text("入学时间不能大于毕业时间");
          errorNode.show();
          return;
        }
        var that = this;
        var data = {
          start_at: start_at,
          end_at: end_at,
          school: that.education.school,
          degree: that.education.degree,
          area: that.education.area,
          detail: that.education.detail
        }
        if (!that.education.id) {
          Service.get('ResumeService').post_education(data).success(function (result) {
            if (result.error_code == 0) {
              Service.get('ResumeService').get_education().success(function (result) {
                if (result.error_code == 0) {
                  that.educations = result.educations;
                  if (!type) {
                    $(".modal02").modal('hide');
                  } else {
                    that.education = {};
                  }

                }
              })
            }
          })
        } else {
          data.eid = that.education.id;
          Service.get('ResumeService').put_education(data).success(function (result) {
            if (result.error_code == 0) {
              Service.get('ResumeService').get_education().success(function (result) {
                if (result.error_code == 0) {
                  that.educations = result.educations;
                  if (!type) {
                    $(".modal02").modal('hide');
                  } else {
                    that.education = {};
                  }
                }
              })
            }
          })
        }


      },
      edit_education: function (item) {
        YWORK.hideErr();
        var that = this;
        that.education = item;
        that.education_start_year = YWORK.time2year(item.start_at);
        that.education_end_year = YWORK.time2year(item.end_at);
        $(".modal02").modal('show');
      },
      save_project: function (type) {
        YWORK.hideErr();
        if (!YWORK.Validator.validateForm($("#project-form"))) {
          return;
        }
        if (this.project_month < 10) {
          this.project_month = "0" + this.project_month
        }
        var finnished_at = this.project_year + "-" + this.project_month;
        var that = this;
        var data = {
          name: that.project.name,
          detail: that.project.detail,
          link: that.project.link,
          picture_id: that.picture.id,
          end_at: finnished_at,
          category_id: that.project.category_id,
        }
        if (!that.project.id) {
          Service.get('ResumeService').post_project(data).success(function (result) {
            if (result.error_code == 0) {
              that.project = {};
              that.picture = {};
              Service.get('ResumeService').get_portfolio().success(function (result) {
                that.projects = result.portfolios;
                if (!type) {
                  $(".modal03").modal('hide');
                  location.reload()
                } else {
                  that.project = {};
                }
              })
            }
          })
        } else {
          data.pid = that.project.id;
          Service.get('ResumeService').put_project(data).success(function (result) {
            if (result.error_code == 0) {
              Service.get('ResumeService').get_portfolio().success(function (result) {
                that.projects = result.portfolios;
                if (!type) {
                  $(".modal03").modal('hide');
                } else {
                  that.project = {};
                }
              })
            }
          })
        }

      },
      edit_project: function (item) {
        YWORK.hideErr();
        var that = this;
        that.project = item;
        this.$set('project_year', YWORK.time2year(item.end_at));
        this.project_month = YWORK.time2month(item.end_at);
        that.project.category_id = item.category.id;
        that.picture = item.picture;
        that.category_pid = item.category.parent_id;
        Service.get('CommonService').category({
          category_id: item.category.parent_id
        }).success(function (result) {
          that.child_category = result.categorys;
        })
        $(".modal03").modal('show');
      },
      do_del_item: function (item, index, type) {
        var that = this;
        if (that.type == "employment") {
          Service.get("ResumeService").delete_employment({
            eid: item.id
          }).success(function (result) {
            if (result.error_code == 0) {
              that.employments.splice(index, 1);
              $("#error").modal('hide');
            }
          });
        } else if (that.type == "education") {
          Service.get("ResumeService").delete_education({
            eid: item.id
          }).success(function (result) {
            if (result.error_code == 0) {
              that.educations.splice(index, 1);
              $("#error").modal('hide');
            }
          });
        } else if (that.type == "project") {
          Service.get("ResumeService").delete_project({
            pid: item.id
          }).success(function (result) {

            console.log(result.error_code);
            if (result.error_code == 0) {
              $("#error").modal('hide');
              location.reload()
            }
          });
        }
      },
      add_item: function (dialog_class) {
        YWORK.hideErr();
        var that = this;
        if (dialog_class == "modal03") {
          that.picture = {
            path: "/static/images/add-project-img.png"
          };
        }
        that.employment = {};
        that.education = {};
        that.project = {};
        var form = $("." + dialog_class).find("form");
        form[0].reset();
        $("." + dialog_class).modal('show');
      },
      del_item: function (item, index, type) {
        if (type) {
          this.item = item;
          this.type = type;
          this.index = index;
          switch (type) {
            case "employment":
              this.errRes = "删除工作经历"
              break;
            case "education":
              this.errRes = "删除教育经历"
              break;
            case "project":
              this.errRes = "删除项目经验"
              break;
            default:
          }
          $("#error").modal('show');
        }
      },
      change_level: function (type) {
        this.level = type;
      },
      prev_category: function () {
        window.location.href = "/users/profile/step/2"
      },
      undate_profile: function () {
        //判断用户的简历是否完善
        var that = this;
        if (that.level == 0 || that.educations.length <= 0) {
          $("#lackprofile").modal('show');
          return;
        }
        Service.get('ResumeService').post_resume({
          level: this.level
        }).success(function (result) {
          if (result.error_code == 0) {
            window.location.href = "/users/profile/step/4";
          }
        })
      },
      picture_upload: function (event) {
        var file = event.target.files[0];
        if (file.size > 5 * 1024 * 1024) {
          this.errPicture = "图片太大";
          return;
        } else {
          this.errPicture = ""
        }
        var data = new FormData();
        var that = this;
        data.append('file', file);
        data.append('_xsrf', Cookies.get('_xsrf'));
        data.append('t', 'portfolio');

        $.ajax({
          type: "POST",
          url: "/api/attachment",
          cache: false,
          dataType: "json",
          data: data,
          processData: false,
          contentType: false,
          success: function (result) {
            if (result.error_code == 0) {
              that.project.picture_id = result.attachment_id;
              that.picture = {
                id: result.attachment_id,
                path: result.path,
                name: result.name
              }
            }
          }
        });
      },
    }
  });
}